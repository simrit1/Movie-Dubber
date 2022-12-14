from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink, QVideoFrame
from PyQt6.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem

from threading import Thread

import ffmpeg
import numpy as np

import main_ui

# FOR NOW: I can make a database of the movies and their attributes and can let people just pick the movie from the database. I'll add the video editor when I learn more.
# https://stackoverflow.com/questions/58816766/how-to-embed-a-pptk-viewer-in-a-pyqt5-window
# https://stackoverflow.com/questions/59015211/how-can-i-add-moviepy-preview-window-inside-pyside2-widget
# Get movie duration (frames/fps), for each in duration: set qmediaplayer position and get frame, then iterate
# Use ffmpeg to get video frames then pipe them to a numpy list. Then try to show it in a PyQt6 widget

class Ui_Editor(QtWidgets.QDialog):
    def __init__(self):
        super().__init__();
        self._alive = True;
        self.setFixedSize(1291, 711);
        self.setWindowTitle('Editor');

        # widget = QtWidgets.QWidget();
        # widget.setGeometry(QtCore.QRect(10, 10, 1271, 541));

        '''Media and audio players and accessories'''
        self.media_player = QMediaPlayer(self);
        # self.display_widget = QtWidgets.QWidget(self);
        # self.display_widget.setGeometry(QtCore.QRect(10, 10, 1271, 541));
        self.video_widget = QVideoWidget(self);
        self.video_widget.setGeometry(QtCore.QRect(10, 10, 1271, 541));
        self.video_sink = self.video_widget.videoSink();
        self.audio_widget = QAudioOutput();
        self.media_player.setSource(QtCore.QUrl.fromLocalFile(main_ui.Ui_MainWindow.video_text_box.text()));
        self.media_player.setVideoSink(self.video_sink);
        # self.media_player.setVideoOutput(self.video_sink);
        self.media_player.setAudioOutput(self.audio_widget);
        # self.media_player.positionChanged.connect(self.set_location_slider);
        # self.media_player.durationChanged.connect(self.duration_changed);
        self.media_player.durationChanged.connect(self.initialize_metadata);
        self.video_sink.videoFrameChanged.connect(self.set_location_slider);
        self.audio_player = QMediaPlayer(self);
        self.audio_widget_2 = QAudioOutput();
        self.audio_player.setAudioOutput(self.audio_widget_2);
        self.audio_player.setSource(QtCore.QUrl.fromLocalFile(main_ui.Ui_MainWindow.audio_text_box.text()));
        self.audio_widget.setVolume(1.00);
        self.audio_widget_2.setVolume(1.00);

        '''Play button'''
        self.play_button = QtWidgets.QPushButton(self);
        self.play_button.setGeometry(QtCore.QRect(10, 558, 32, 24));
        self.play_icon = QtGui.QIcon();
        self.play_icon.addFile("theme/play_pause_icon_137298.png");
        self.play_button.setIcon(self.play_icon);
        self.play_button.setIconSize(QtCore.QSize(25, 25));
        self.play_button.clicked.connect(self.play_pause);

        '''Restart button'''
        self.restart_button = QtWidgets.QPushButton(self);
        self.restart_button.setGeometry(QtCore.QRect(50, 558, 32, 24));
        self.restart_button.setText('R/V');
        self.restart_button.clicked.connect(self.set_video_to_beginning);

        '''Restart both video and audio button'''
        self.restart_both_button = QtWidgets.QPushButton(self);
        self.restart_both_button.setGeometry(QtCore.QRect(90, 558, 32, 24));
        self.restart_both_button.setText('R/B');
        self.restart_both_button.clicked.connect(self.restart_audio_and_video);

        '''Restart everything button'''
        self.restart_everything_button = QtWidgets.QPushButton(self);
        self.restart_everything_button.setGeometry(QtCore.QRect(130, 558, 32, 24));
        self.restart_everything_button.setText("R/E");
        self.restart_everything_button.clicked.connect(self.restart_everything);

        '''Movie volume and divider'''
        self.movie_volume_label = QtWidgets.QLabel(self);
        self.movie_volume_label.setGeometry(QtCore.QRect(684, 565, 78, 13));
        self.movie_volume_label.setText('Movie Volume:');
        self.movie_volume = QtWidgets.QSlider(self);
        self.movie_volume.setGeometry(QtCore.QRect(767, 561, 200, 25));
        self.movie_volume.setRange(0, 100);
        self.movie_volume.setPageStep(5);
        self.movie_volume.setSliderPosition(50);
        self.movie_volume.setTracking(True);
        self.movie_volume.setOrientation(QtCore.Qt.Orientation.Horizontal);
        self.movie_volume.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBothSides);
        self.movie_volume.valueChanged.connect(self.change_volume);
        self.divider = QtWidgets.QFrame(self);
        self.divider.setGeometry(QtCore.QRect(985, 561, 3, 23));
        self.divider.setFrameShape(QtWidgets.QFrame.Shape.VLine);

        '''Attenuation label and slider'''
        self.attenuation_label = QtWidgets.QLabel(self);
        self.attenuation_label.setGeometry(QtCore.QRect(1000, 565, 65, 13));
        self.attenuation_label.setText('Attenuation:');
        self.attenuation_slider = QtWidgets.QSlider(self);
        self.attenuation_slider.setGeometry(QtCore.QRect(1071, 561, 200, 25));
        self.attenuation_slider.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight);
        self.attenuation_slider.setMinimum(-10);
        self.attenuation_slider.setMaximum(10);
        self.attenuation_slider.setPageStep(1);
        self.attenuation_slider.setProperty("value", 0);
        self.attenuation_slider.setSliderPosition(0);
        self.attenuation_slider.setTracking(True);
        self.attenuation_slider.setOrientation(QtCore.Qt.Orientation.Horizontal);
        self.attenuation_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBothSides);

        '''Location slider and box'''
        self.location_slider = QtWidgets.QSlider(self);
        self.location_slider.setGeometry(QtCore.QRect(10, 580, 1191, 41));
        self.location_slider.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight);
        self.location_slider.setMinimum(0);
        self.location_slider.setOrientation(QtCore.Qt.Orientation.Horizontal);
        self.location_slider.sliderMoved.connect(self.playback_position);
        self.location_box = QtWidgets.QSpinBox(self);
        self.location_box.setMinimum(0);0
        self.location_box.setGeometry(QtCore.QRect(1210, 590, 61, 22));

        '''Movie track slider, label, and spinbox'''
        self.movie_track_slider = QtWidgets.QSlider(self);
        self.movie_track_slider.setGeometry(QtCore.QRect(10, 620, 1191, 41));
        self.movie_track_slider.setOrientation(QtCore.Qt.Orientation.Horizontal);
        # self.movie_track_slider.setMaximum(9999999);
        self.movie_track_slider.valueChanged.connect(self.adjust_movie_track_spinbox);
        self.movie_delay_label = QtWidgets.QLabel(self);
        self.movie_delay_label.setGeometry(QtCore.QRect(1208, 610, 65, 15));
        self.movie_delay_label.setText('Movie delay');
        self.movie_delay_label.setToolTip('Movie delay in ms, to fine tune movie position.');
        self.movie_track_spinbox = QtWidgets.QSpinBox(self);
        self.movie_track_spinbox.setGeometry(QtCore.QRect(1210, 630, 66, 22));
        # self.movie_track_spinbox.setMaximum(9999999);
        self.movie_track_spinbox.setToolTip('Movie delay in ms, to fine tune movie position.');
        self.movie_track_spinbox.valueChanged.connect(self.media_player_delay);

        # self.get_frames();
        '''Execute ui initiation'''
        self.exec();

    #################
    #|  FUNCTIONS  |#
    #################

    def initialize_metadata(self):
        self.probe = ffmpeg.probe(main_ui.Ui_MainWindow.video_text_box.text());
        self.video_info = next(s for s in self.probe['streams'] if s['codec_type'] == 'video');
        self.width = int(self.video_info['width']);
        self.height = int(self.video_info['height']);
        try: 
            self.num_frames = int(self.video_info['nb_frames']); # Doesn't work for mkv files
            print(self.num_frames);
        except: pass;
        # self.out = (
        #         ffmpeg
        #         .input(main_ui.Ui_MainWindow.video_text_box.text())
        #         .output('pipe:', c='copy', f='null')
        #         .run(capture_stdout=True)
        # );
        # self.video = (
        #     np
        #     .frombuffer(self.out, np.uint8)
        #     .reshape([-1, self.height, self.width, 3])
        # );
        # stream = ffmpeg.Stream(ffmpeg.input(main_ui.Ui_MainWindow.video_text_box.text()));
        #####################
        self.movie_duration = self.media_player.duration();
        self.audio_duration = self.audio_player.duration();
        if self.movie_duration > self.audio_duration:
            self.location_slider.setMaximum(self.movie_duration);
            self.location_box.setMaximum(self.movie_duration);
        else:
            self.location_slider.setMaximum(self.audio_duration);
            self.location_box.setMaximum(self.audio_duration);
        # self.location_slider.setMaximum(self.movie_duration);
        self.movie_track_slider.setMaximum(self.movie_duration);
        self.movie_track_spinbox.setMaximum(self.movie_duration);
        self.first_frame = self.video_sink.videoFrame();

    def pause_media_and_audio(self):
        self.media_player.pause();
        self.audio_player.pause();

    def load_video_to_memory(self):
        pass;

    def set_video_to_beginning(self):
        self.audio_player.pause();
        self.media_player.pause();
        self.media_player.setPosition(0);

    def restart_audio_and_video(self):
        self.media_player.pause();
        self.audio_player.pause();
        self.media_player.setPosition(0);
        self.audio_player.setPosition(0);

    def restart_everything(self):
        self.pause_media_and_audio();
        self.media_player.setPosition(0);
        self.audio_player.setPosition(0);
        self.location_slider.setValue(0);
        self.location_box.setValue(0);
        self.movie_track_slider.setValue(0);
        self.movie_track_spinbox.setValue(0);

    def set_location_slider(self):
        # self.video_sink.videoFrame();
        # print('new frame');
        # self.location_slider.setValue(self.video_sink.videoFrame);
        self.location_slider.setValue(self.media_player.position());
        self.location_box.setValue(self.media_player.position());

    def playback_position(self):
        self.pause_media_and_audio();
        self.media_player.setPosition(self.location_slider.value());
        self.audio_player.setPosition(self.location_slider.value());

    def change_volume(self):
        vol = float(self.movie_volume.value());
        vol = round(vol/100, 4);    ## Shift vol value 2 decimal places to the left
        # print(f'{vol} ========== {type(vol)}');
        self.audio_widget.setVolume(vol);
        # self.audio_widget_2.setVolume(vol);

    def play_pause(self):
        if self.media_player.playbackState().value == 1:
            self.pause_media_and_audio();
        else:
            self.audio_player.play();
            self.play_media = Thread(target=self.play_media_when_match_delay);
            self.play_media.start();
            # self.play_media_when_match_delay();
            # self.media_player.play();

    def play_media_when_match_delay(self):
        # while self._alive == True:
        while self.audio_player.position() < self.movie_track_spinbox.value():
            if self.media_player.playbackState() == 1:
                self.media_player.pause();
            else:
                pass;
        if self.audio_player.position() >= self.movie_track_spinbox.value():
            self.media_player.play();

    def media_player_delay(self):
        # self.blankie = QVideoFrame();
        # self.blankie.map(self.blankie.MapMode.ReadWrite);
        # self.first_frame.map(QVideoFrame.MapMode.ReadWrite);
        # self.first_frame.setStartTime(self.movie_track_spinbox.value() * 100);
        # self.first_frame.setEndTime(100);
        self.first_frame.setEndTime(self.movie_track_spinbox.value());
        # self.video_sink.setVideoFrame(self.first_frame);
        # print(self.first_frame.mapMode());
        if self.media_player.playbackState() == 1 or self.audio_player.playbackState() == 1:
            self.pause_media_and_audio();
        # movie_delay = self.movie_track_spinbox.value();

    def play_video(self):
        while self.audio_player.position() != self.movie_track_spinbox.value():
            pass;
        if self.audio_player.position() >= self.movie_track_spinbox.value():
            self.media_player.play();

    def adjust_movie_track_spinbox(self):
        self.movie_track_spinbox.setValue(self.movie_track_slider.value());

    def confirm_options(self):
        # For when I make a confirm button
        pass;

    def terminate(self):
        print('bye');