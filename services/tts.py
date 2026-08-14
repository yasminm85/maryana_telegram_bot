import edge_tts

async def text_to_speech(text: str, output_path: str = "response.mp3") -> str:
    try:
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error on Edge TTS: {e}")
        return ""