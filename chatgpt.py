import logging

import os
from pathlib import Path

from openai import OpenAI

from log import log_debug

OPENAI_API_KEY = "OPENAI_API_KEY"


class ChatGpt():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv(OPENAI_API_KEY)
        )

    @log_debug
    def get_response(self, request: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": request},
            ]
        )
        logging.info(completion.choices[0].message.content)
        return completion.choices[0].message.content

    @log_debug
    def text_to_speech(self, text: str) -> Path:
        speech_file_path = Path(__file__).parent / "speech.mp3"

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )

        response.stream_to_file(speech_file_path)
        return speech_file_path

    @log_debug
    def speech_to_text(self, audio_input: Path) -> str:
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_input.absolute()
        )
        return transcription.text

    @log_debug
    def process_request(self, request, tools, processors) -> None:
        logging.info(f"Processing request {request}")
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Based on user request Generate one of the following commands: {', '.join(processors.keys())}. In case of unsertancy "},
                {"role": "user", "content": request},
            ],
            tools=tools,
        )
        logging.info(f"Response: {completion.choices[0].message}")
        logging.debug(f"Processor: {completion.choices[0].message.tool_calls[0].function.name}")

        processor = processors.get(completion.choices[0].message.tool_calls[0].function.name)
        processor.process_request(request, self)