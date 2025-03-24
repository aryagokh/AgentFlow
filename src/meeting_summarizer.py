from components.video_to_audio import convert_video_to_audio_moviepy
from components.audio_to_text import audio_to_text
from components.summary_generator import summary_generator
# Mail them
from fastapi import FastAPI, UploadFile, File
import uvicorn
import sys
import os

app = FastAPI()

@app.post("/summarize_video/")
async def upload_video(file: UploadFile = File(...)):
    """Handles video upload, extracts audio, transcribes, and summarizes."""
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(file.file.read())
    
    try:
        audio_path = convert_video_to_audio_moviepy(video_path)
        transcription = audio_to_text(audio_path)
        summary = summary_generator('Meeting summarizer', transcription, additional_details=None)
        os.remove(audio_path)
        os.remove(video_path)
        return summary
    except Exception as e:
        print("Exception:", e)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


