from src import wikiapi
from src.title2vec import Title2Vec, EmbeddedTitle
import numpy as np
import pywikibot
from src.traverse.traverse import Traverse


class SimilarTraverse(Traverse):
    def __init__(self, start_subject: str, target_subject: str) -> None:
        """
        Constructor for SimilarTraverse.

        This algorithm uses the pretrained gensim Word2Vec model
        to estimate the similarities between two titles and move accordingly.

        Args:
            start_subject (str): the starting subject to navigate to the target subject from. 
            target_subject (str): the subject we are trying to get to from the starting point.
        """

        super(SimilarTraverse, self).__init__(start_subject)
        self._target = target_subject

        self._active_page = wikiapi.generate_wiki_page_from_title(
            start_subject)
        self._t2v = Title2Vec()

        self._target_embedded = self._t2v.embed_title(target_subject)

    def target_found(self) -> bool:
        """
        Has the target been reached in the graph?

        Returns:
            bool: the target has been reached if true.
        """

        return self._graph.node_exists(self._target)

    def traverse(self):
        """
        This algorithm works as follows:
        1. Loop through all outgoing links for the current page.
        2. For each link do steps 3-6
        3. Add link to the graph.
        4. Embed the link using pre-trained Word2Vec model.
        5. Calculate similarity between link and title.
        6. Save link if its the most similar page encountered so far.
        7. Select the most similar page as the next node.
        """

        top_score, top_page = -1, pywikibot.Page("")

        # Find the node connected to this page with the highest similarity
        for link in wikiapi.retrieve_outgoing_links(self._active_page):
            # Don't revisit past nodes.
            if link.title() in self._trace:
                continue

            # Inform the graph of this new connection
            self._graph.new_edge(self._subject, link.title())

            # Embed the title.
            embedded_title = self._t2v.embed_title(link.title())
            if len(embedded_title) == 0:
                continue

            # Calculate the similarity between the two titles.
            sim_score = self.title_sim_score(
                self._target_embedded, embedded_title)
            # Save the current link if it has the highest similarity score.
            if sim_score > top_score:
                top_score = sim_score
                top_page = link

        # Move to the most similar page.
        self._subject = top_page.title()
        self._active_page = top_page
        self._trace.append(top_page.title())

    def title_sim_score(self, title1: EmbeddedTitle, title2: EmbeddedTitle) -> float:
        """
        For the NLP domain, this code utilizes the cosine similarity.

        Args:
            title1 (EmbeddedTitle): the first embedded title.
            title2 (EmbeddedTitle): the second embedded title.

        Returns:
            float: the cosine similarity between the two given titles.
        """

        A = title1.get_vectors()
        B = title2.get_vectors()

        dot = np.dot(A, B.T)

        A_norm = np.linalg.norm(A, axis=1)
        B_norm = np.linalg.norm(B, axis=1)

        A_norm = A_norm.reshape(-1, 1)
        B_norm = B_norm.reshape(1, -1)

        sim_mat = dot / A_norm
        sim_mat = sim_mat / B_norm

        return np.mean(np.max(sim_mat, axis=1))
