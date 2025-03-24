import os
from dotenv import load_dotenv
import google.genai as genai
load_dotenv()

def audio_to_text(audio_file):
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        myfile = client.files.upload(file=audio_file)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=['Transcribe this audio clip', myfile]
        )
        client.files.delete(name=myfile.name)
        return response.text
    except Exception as e:
        print(e)
        return -1

# if __name__ == '__main__':
#     print(audio_to_text('data/raw/videos/Short_Meet.mp3'))