# import required libraries
import datetime
import logging

import numpy as np
import sounddevice as sd
from pathlib import Path
import pygame
from log import log_debug

from audiorecord import AudioRecord


class Audio:
    def __init__(self):
        self.recording_data = []  # Buffer for recording audio
        self.silence_start_time = None  # Time when silence started

    @log_debug
    def record_audio(self) -> AudioRecord:
        logging.info("Recording audio...")

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

        # Convert the NumPy array to audio file
        logging.info("Audio recorded")
        return AudioRecord(recording, freq)


    @staticmethod
    @log_debug
    def play_audio(file: Path) -> None:
        logging.info("Playing audio...")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        logging.debug("Audio is playing...")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        logging.debug("Audio played")

    @staticmethod
    def is_silence(data, threshold) -> bool:
        # Function to check volume level (silence detector)
        return np.abs(data).mean() < threshold

    @log_debug
    def record_audio_while_speaking(self) -> AudioRecord:
        logging.info("Recording audio while speaking...")
        # Recording parameters
        sample_rate = 44100  # Sampling frequency
        channels = 1  # One channel (mono)
        silence_threshold = 500  # Volume threshold for detecting silence
        max_silence_duration = datetime.timedelta(seconds=1)  # Maximum duration of silence (seconds)
        block_duration = 100 # ms

        def callback(indata, frames, t, status):
            if status:
                logging.info(status)

            # Add recorded data to buffer
            self.recording_data.append(indata.copy())

            # Check if there is sound
            if not self.is_silence(indata, silence_threshold):
                self.silence_start_time = None  # If there is sound, reset the silence timer
            else:
                logging.debug("Silence detected. Stopping recording.")
                # If silence and the timer is not started, start it
                if self.silence_start_time is None:
                    self.silence_start_time = datetime.datetime.now()
                # If silence continues for too long, stop recording
                elif datetime.datetime.now() - self.silence_start_time > max_silence_duration:
                    logging.info("Silence detected. Stopping recording.")
                    sd.stop()

        # Start recording
        logging.info("Recording started... Speak!")
        self.silence_start_time = None
        with sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate, blocksize=int(sample_rate * block_duration / 1000), dtype='int16'):
            sd.sleep(10000)  # Wait up to 10 seconds (or less if silence is detected)

        recording_data = np.concatenate(self.recording_data)

        logging.info("Recording finished")
        return AudioRecord(recording_data, sample_rate)
