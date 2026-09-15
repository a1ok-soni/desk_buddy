import subprocess
import tempfile
import wave

from piper import PiperVoice

_voice = PiperVoice.load("voices/en_US-joe-medium.onnx")


def speak(text: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        with wave.open(f.name, "wb") as wav_file:
            _voice.synthesize_wav(text, wav_file)
        subprocess.run(["afplay", f.name], check=True)
