from abc import abstractmethod

from chatgpt import ChatGpt


class Processor:
    @abstractmethod
    def process_request(self, request: str, ai: ChatGpt):
        pass
