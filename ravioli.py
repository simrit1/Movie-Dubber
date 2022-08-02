from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QLabel, QPushButton, QDialog


    #########################
    #|  Custom Exceptions  |#
    #########################

class OutputLoadError(Exception):
    pass;

class VideoLoadError(Exception):
    pass;

class AudioLoadError(Exception):
    pass;

class MissingFFMPEG(Exception):
    pass;

    #####################
    #|  Error Dialogs  |#
    #####################

class Ui_Error_Output_Load(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('Output Location Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must select an output folder');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.reject)
        '''Run'''
        self.exec();

class Ui_Error_Delay(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('Delay Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must provide delay in milliseconds');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.reject)
        '''Run'''
        self.exec();

class Ui_Error_Video_load(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('Video File Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must select a video file to sync');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.accept)
        '''Run'''
        self.exec();

class Ui_Error_Audio_load(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('Audio File Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must select an audio file to sync');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.accept)
        '''Run'''
        self.exec();

class Ui_Error_load_from_database(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('Database Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must select a movie from database');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.accept)
        '''Run'''
        self.exec();

class Ui_Error_FFMPEG_required(QDialog):
    def __init__(self):
        super().__init__();
        self.setWindowTitle('FFMPEG Error');
        self.setFixedSize(226, 58);
        '''Message Text'''
        self.message = QLabel(self);
        self.message.setText('You must have FFMPEG in PATH, or MovieDubber root directory.');
        self.message.setGeometry(QRect(10, 6, 208, 20));
        '''Okay button'''
        self.okay = QPushButton('Okay', self);
        self.okay.setGeometry(QRect(82, 31, 61, 21));
        self.okay.clicked.connect(self.accept)
        '''Run'''
        self.exec();
