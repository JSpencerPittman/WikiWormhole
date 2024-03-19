from src import wikiapi
from embed.title2vec import Title2Vec, VectorizedTitle
from score.similar import title_similarity
from traversal.table import WikipageTable


class SimilarTraversal(object):
    def __init__(self, start_subject, target_subject):
        self.subject = start_subject
        self.target = target_subject
        self.trace = [start_subject]

        self.page = wikiapi.generate_wiki_page_from_title(start_subject)

        self.t2v = Title2Vec()

        self.target_vectorized = self.t2v.title_to_vector(target_subject)

        self.blacklist = list()

        self.table = WikipageTable(start_subject)

    def found(self):
        return self.table.entry_exists(self.target)

    def safe_traversal(self):
        traversed = False

        while not traversed:
            try:
                self.traverse()
                traversed = True
            except AttributeError:
                self.blacklist.append(self.subject)

                self.trace.pop()
                self.subject = self.trace[-1]
                self.page = wikiapi.generate_wiki_page_from_title(
                    self.subject)

    def traverse(self):
        top_score = None
        top_page = None

        for link in wikiapi.retrieve_outgoing_links(self.page):
            if link.title() in self.trace or link.title() in self.blacklist:
                continue

            self.table.spot(link.title(), self.subject)

            vectorized = self.t2v.title_to_vector(link.title())
            if len(vectorized) == 0:
                continue
            sim_score = title_similarity(vectorized, self.target_vectorized)
            if top_score is None or sim_score > top_score:
                top_score = sim_score
                top_page = link

        self.page = top_page
        self.subject = top_page.title()

        print(f"{self.trace} -> {self.subject}")

        self.trace.append(self.subject)
