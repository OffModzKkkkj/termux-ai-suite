from gtts import gTTS
import os

def generate_audio(text, output_path="assets/narration.mp3"):
    tts = gTTS(text=text, lang='pt')
    tts.save(output_path)
    return output_path
