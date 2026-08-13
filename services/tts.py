import edge_tts

async def text_to_speech(text: str, output_path: str = "response.mp3") -> str:
    """
    Mengubah teks menjadi voice note menggunakan Microsoft Edge TTS (Gratis & Natural).
    """
    try:
        # Pilihan suara natural: en-US-AriaNeural atau en-US-GuyNeural
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error pada Edge TTS: {e}")
        return ""