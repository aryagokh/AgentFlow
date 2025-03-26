import os
import google.genai as genai
import assemblyai as aai
from dotenv import load_dotenv
from config import get_secret
load_dotenv()

aai.settings.api_key = get_secret('ASSEMBLYAI_API_KEY')

def transcribe_the_video(video_path):
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(video_path)
        return transcript.text
    except Exception as e:
        print(e)
        return -1
    
# if __name__ == '__main__':
#     print(transcribe_the_video(
#         video_path='data/raw/videos/Short_Meet.mp4'
#     ))