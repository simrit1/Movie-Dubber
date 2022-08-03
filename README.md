# Movie Dubber
Right now, this is just a GUI to run an ffmpeg command to overlay an audio track on a video file; intended for movies and dubs. Later, I'd like to fix the (disabled for now) video editor so you could sync movies and dubs without having to load from the database. 

Please excuse the mess, as I'm still new to programming, this is my first program.

## Things you should know
- Some videos (like some older movies) don't like their audio being messed with. So the output file would be out of sync. Try a different movie file.
- Not all movies in the database currently have a Delay. They are not usable right now.

## Screenshots
<details>
  <summary>Screenshots</summary>

  ![Main Screen](https://github.com/f09f9095/Movie-Dubber/blob/main/etc/Main%20Screen.png?raw=true)
  ![Database](https://github.com/f09f9095/Movie-Dubber/blob/main/etc/Database.png?raw=true)
</details>


## Instructions
Things you'll need:
- ffmpeg [added to your path](https://www.youtube.com/watch?v=3z9rUl9r2oA) - [Windows](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
  - You may also take the ffmpeg.exe from ffmpeg-git-full zip and put it in the root folder of the Movie Dubber exe (or __init__.py if running from source).
- A movie file that **_matches the Length_** of the listed movie in the database.
  - The only working movies are ones in the database with a Delay listed. The database will be updated when I can.
- An audio track to lay over the movie

Steps:
>1. Select output folder where movie will be saved
>2. Select input movie file (Should match movie duration (Length) in database for proper sync)
>3. Select input audio track
>4. Adjust volume and ratio options if desired - I recommend using ratio
>5. Select movie to be synced from database (Must have Delay)
>6. Press Encode

Options:
- Delay (ms): In this box you enter how long to delay the added audio track.
  - This option is usually added from the database unless you know how syncronized the dubs yourself.
- Volume: This box allows you to change the movie file volume level.
  - Entered value should be an (+/-) integer. Value will adjust movie decible level.
- Ratio: Ratio allows you to have the added audio track take precidence over the movie.
  - Valid entries: 1 to 9.99
  - Example: Setting Ratio to 2.5 will mean the movie audio will lower itself 2.5x while the added audio track is producing audio (talking).
