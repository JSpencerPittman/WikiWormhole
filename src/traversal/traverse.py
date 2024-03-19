from abc import ABC, abstractmethod


class Traverse(ABC):
    def __init__(self, start_subject: str):
        self._subject = start_subject
        self._trace = [start_subject]

    @abstractmethod
    def traverse(self):
        pass
