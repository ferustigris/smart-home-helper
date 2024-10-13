# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
import pygame


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
