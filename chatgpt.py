import os
from pathlib import Path

from openai import OpenAI

OPENAI_API_KEY = "OPENAI_API_KEY"

class ChatGpt():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv(OPENAI_API_KEY)
        )

    def get_response(self, request: str) -> str:
        global completion
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": request},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    def text_to_speech(self, text: str) -> Path:
        speech_file_path = Path(__file__).parent / "speech.mp3"

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )

        response.stream_to_file(speech_file_path)
        return speech_file_path

    def speech_to_text(self, audio_input: Path) -> str:
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_input.absolute()
        )
        return transcription.text
