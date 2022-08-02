# MovieDubber
Right now, this is just a GUI to run a dynamic ffmpeg command to overlay an audio track on a video file. Intended for movies and dubs.

Please excuse the mess, as I'm still new to programming.

## Things you should know
- Some videos (like some older movies) don't like their audio being messed with. So the output file would be out of sync. Try a different movie file.
- 

## Screens
![MainScreen](https://github.com/f09f9095/MovieDubber/blob/master/etc/MainScreen.png?raw=true)
![Editor](https://github.com/f09f9095/MovieDubber/blob/master/etc/Editor.png?raw=true)

## Instructions
Things you'll need (until I fix the editor):
- A video editor with a timeline like [ShotCut](https://github.com/mltframework/shotcut/releases/tag/v22.04.25)
- ffmpeg [added to your path](https://duckduckgo.com/?t=ffab&q=add+to+path+windows&atb=v255-1&ia=web) - [Windows](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
- A video or movie and an audio track to add

Step one:
```
- Open ShotCut and add the video the timeline at the bottom.
- Right click the time line and add an audio track (or alt+u)
