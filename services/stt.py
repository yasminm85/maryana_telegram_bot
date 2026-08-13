import os
from groq import Groq

def transcribe_audio(file_path: str) -> str:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model="whisper-large-v3",
                language="en"
            )
        return transcription.text.strip()
    except Exception as e:
        print(f"Error STT Groq: {e}")
        return ""