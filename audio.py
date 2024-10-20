# import required libraries
import datetime

import numpy as np
import sounddevice as sd
from scipy._lib._ccallback import CData
from scipy.io.wavfile import write
from pathlib import Path
import pygame

from audiorecord import AudioRecord


class Audio:
    def __init__(self):
        self.recording_data = []  # Buffer for recording audio
        self.silence_start_time = None  # Time when silence started

    def record_audio(self) -> Path:
        print("Recording audio...")

        # Sampling frequency
        freq = 44100

        # Recording duration
        duration = 5

        # Start recorder with the given values
        # of duration and sample frequency
        recording = sd.rec(int(duration * freq),
                           samplerate=freq, channels=1)

        # Record audio for the given number of seconds
        sd.wait()

        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        speech_file_path = Path(__file__).parent / "recording0.wav"
        write(speech_file_path, freq, recording)

        # Convert the NumPy array to audio file
        print("Audio recorded")
        return speech_file_path


    def play_audio(self, file: Path) -> None:
        print("Playing audio...")
        # Load the audio file
        # from playsound import playsound
        # playsound(file.absolute())
        # samplerate, data = read(file)
        # # Play the audio file
        # sd.play(data)
        # sd.wait()

        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        print("Audio is playing...")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("Audio played")

    def is_silence(self, data, threshold) -> bool:
        # Function to check volume level (silence detector)
        return np.abs(data).mean() < threshold

    def record_audio_while_speaking(self):
        import sounddevice as sd
        import numpy as np

        # Recording parameters
        sample_rate = 44100  # Sampling frequency
        channels = 1  # One channel (mono)
        silence_threshold = 50  # Volume threshold for detecting silence
        max_silence_duration = datetime.timedelta(seconds=2)  # Maximum duration of silence (seconds)
        block_duration = 100 # ms

        def callback(indata, frames, t: CData, status):
            if status:
                print(status)

            # Add recorded data to buffer
            self.recording_data.append(indata.copy())

            # Check if there is sound
            if not self.is_silence(indata, silence_threshold):
                self.silence_start_time = None  # If there is sound, reset the silence timer
            else:
                # If silence and the timer is not started, start it
                if self.silence_start_time is None:
                    self.silence_start_time = datetime.datetime.now()
                # If silence continues for too long, stop recording
                elif datetime.datetime.now() - self.silence_start_time > max_silence_duration:
                    print("Silence detected. Stopping recording.")
                    sd.stop()

        # Start recording
        print("Recording started... Speak!")
        self.silence_start_time = None
        with sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate, blocksize=int(sample_rate * block_duration / 1000), dtype='int16'):
            sd.sleep(10000)  # Wait up to 10 seconds (or less if silence is detected)

        # Save to WAV file
        recording_data = np.concatenate(self.recording_data)
        # recording_data = np.array(self.recording_data, dtype='int16')
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        speech_file_path = Path(__file__).parent / "recording1.wav"
        write(speech_file_path, sample_rate, recording_data)

        print("Recording finished and saved to output.wav")
        return speech_file_path
