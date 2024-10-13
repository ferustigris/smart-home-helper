from audio import record_audio, play_audio
from chatgpt import ChatGpt

audio_input = record_audio()

# Create an instance of the ChatGpt class
# https://platform.openai.com/docs/quickstart?language-preference=python
# Billing: https://platform.openai.com/settings/organization/billing/overview
ai = ChatGpt()

request = ai.speech_to_text(audio_input)
response = ai.get_response(request)

speech_file_path = ai.text_to_speech(response)
play_audio(speech_file_path)
