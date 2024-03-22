from abc import ABC, abstractmethod
from src.traverse.graph import SearchGraph


class Traverse(ABC):
    def __init__(self, start_subject: str):
        self._subject = start_subject
        self._trace = [start_subject]
        self._graph = SearchGraph(start_subject)

    @abstractmethod
    def traverse(self):
        pass
