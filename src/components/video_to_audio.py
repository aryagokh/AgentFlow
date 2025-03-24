from moviepy import VideoFileClip
import os

def convert_video_to_audio_moviepy(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    try:
        filename, ext = os.path.splitext(video_file)
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(f"{filename}.{output_ext}")
        return f'{filename}.{output_ext}'
    except Exception as e:
        print(e)
        return -1


# if __name__ == '__main__':
#     print(convert_video_to_audio_moviepy(
#         video_file='data/raw/videos/Short_Meet.mp4'
#     ))