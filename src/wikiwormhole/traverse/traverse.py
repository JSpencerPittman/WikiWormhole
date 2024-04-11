from abc import ABC, abstractmethod
from wikiwormhole.util.graph import ConnectionGraph
from typing import List
from wikiwormhole import wikiapi
from pywikibot import Page


class Traverse(ABC):
    def __init__(self, start_subject: str):
        self._active_subject: str = start_subject
        self._active_page: Page = wikiapi.generate_wiki_page_from_title(
            start_subject)

        if not self._active_page.exists():
            raise Exception(
                'Traverse: please provide a traverse page that exists.')

        self._trace: List[str] = [start_subject]
        self._graph: ConnectionGraph[str] = ConnectionGraph[str](start_subject)

    @abstractmethod
    def traverse(self):
        pass

    @staticmethod
    def valid_page(title: str):
        title = title.lower()
        if 'wayback' in title or 'identifier' in title:
            return False
        return True
