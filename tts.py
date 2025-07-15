# tts.py

from gtts import gTTS
import pygame
import tempfile
import os

def speak(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

        pygame.mixer.music.unload()
        pygame.mixer.quit()
        os.remove(temp_path)

    except Exception as e:
        print(f"TTS Error: {e}")
