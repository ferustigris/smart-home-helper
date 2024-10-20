import logging

from audiorecord import AudioRecord
from audio import Audio
from chatgpt import ChatGpt
from log import log_debug

from processor import Processor


tools = [
    {
        "type": "function",
        "function": {
            "name": "shutdown",
            "description": "Shutdown the system",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "response_processing",
            "description": "Process the user request",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        }
    }
]


class ShutdownProcessor(Processor):
    @log_debug
    def process_request(self, request: str, ai: ChatGpt):
        logging.info(f"Shutdown the system by request {request}")
        exit(0)


class UserRequestPrcoessor(Processor):
    @log_debug
    def process_request(self, request: str, ai: ChatGpt):
        logging.info(f"User Request processing: {request}")
        response = ai.get_response(request)

        speech_file_path = ai.text_to_speech(response)
        Audio.play_audio(speech_file_path)


processors = {
    "shutdown" : ShutdownProcessor(),
    "response_processing": UserRequestPrcoessor(),
}

while True:
    audio = Audio()
    # audio_input = audio.record_audio()
    audio_input: AudioRecord = audio.record_audio_while_speaking()
    if audio.is_silence(audio_input.get_data(), 50):
        logging.debug("There is no data recorded!")
        continue

    audio_input.save()

    # Create an instance of the ChatGpt class
    # https://platform.openai.com/docs/quickstart?language-preference=python
    # Billing: https://platform.openai.com/settings/organization/billing/overview
    ai = ChatGpt()

    request = ai.speech_to_text(audio_input.get_file_path())

    ai.process_request(request, tools, processors)
