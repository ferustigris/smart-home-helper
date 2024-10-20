# import required libraries
import datetime

import sounddevice as sd
from scipy._lib._ccallback import CData
from scipy.io.wavfile import write
from pathlib import Path
import pygame

recording_data = []  # Buffer for recording audio
silence_start_time = None  # Time when silence started

def record_audio() -> Path:
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


def play_audio(file: Path) -> None:
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

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        print("Audio is playing...")
    print("Audio played")


def record_audio_while_speaking() -> Path:
    import sounddevice as sd
    import numpy as np

    # Recording parameters
    sample_rate = 44100  # Sampling frequency
    channels = 1  # One channel (mono)
    silence_threshold = 500  # Volume threshold for detecting silence
    max_silence_duration = datetime.timedelta(seconds=2)  # Maximum duration of silence (seconds)

    # Function to check volume level (silence detector)
    def is_silence(data, threshold):
        return np.abs(data).mean() < threshold

    def callback(indata, frames, t: CData, status):
        global silence_start_time, recording_data

        if status:
            print(status)

        # Add recorded data to buffer
        recording_data.extend(indata)

        # Check if there is sound
        if not is_silence(indata, silence_threshold):
            silence_start_time = None  # If there is sound, reset the silence timer
        else:
            # If silence and the timer is not started, start it
            if silence_start_time is None:
                silence_start_time = datetime.datetime.now()
            # If silence continues for too long, stop recording
            elif datetime.datetime.now() - silence_start_time > max_silence_duration:
                print("Silence detected. Stopping recording.")
                sd.stop()

    # Start recording
    print("Recording started... Speak!")
    silence_start_time = None
    with sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate, dtype='int16'):
        sd.sleep(10000)  # Wait up to 10 seconds (or less if silence is detected)

    # Save to WAV file
    recording_data = np.array(recording_data, dtype='int16')
    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    speech_file_path = Path(__file__).parent / "recording1.wav"
    write(speech_file_path, sample_rate, recording_data)

    print("Recording finished and saved to output.wav")
    return speech_file_path
