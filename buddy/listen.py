import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

_model = WhisperModel("base.en", device="cpu", compute_type="int8")

SAMPLE_RATE = 16000


def listen() -> str:
    input("Press Enter to start talking...")
    print("Listening... press Enter to stop.")

    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback
    ):
        input()

    audio = np.concatenate(recording, axis=0).flatten()
    segments, _ = _model.transcribe(audio, language="en")
    text = " ".join(segment.text for segment in segments).strip()

    print(f"You said: {text}")
    return text
