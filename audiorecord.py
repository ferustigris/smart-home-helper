import ctypes

import numpy as np
from scipy.io.wavfile import write, read
from pathlib import Path

class AudioRecord:
    def __init__(self, audio_data, sample_rate):
        self.sample_rate = sample_rate
        self.recording_data = audio_data
        self.file_name = None

    def save(self) -> Path:
        # Save to WAV file
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        self.file_name = Path(__file__).parent / "recording1.wav"
        write(self.file_name, self.sample_rate, self.recording_data)
        return self.file_name

    def load(self) -> None:
        self.sample_rate, self.recording_data = read(Path(__file__).parent / "recording1.wav")

    def get_file_path(self) -> Path:
        if not self.file_name:
            # TODO: Do I need it?
            return  self.save()
        return self.file_name

    def get_data(self) -> ctypes.Array:
        if self.recording_data is None:
            self.load()
        return self.recording_data