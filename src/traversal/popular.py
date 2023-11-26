from wikiapi import wikipage
from wikiapi.pageviews import get_page_views
from score.popular import outgoing_links
import numpy as np
import constants
from traversal.table import WikipageTable

class PopularTraversal(object):
    def __init__(self, start_subject):
        self.subject = start_subject
        self.trace = [start_subject]

        self.page = wikipage.get_wikipedia_page_from_title(start_subject) 

        self.table = WikipageTable(start_subject)

    def traverse(self):
        self._save_outgoing_connections()

        if len(self.table) == 1:
            raise Exception(f"Please provide a valid page title: {self.trace[0]}")

        rand_idxs = np.random.randint(0, len(self.table)-1, constants.POP_BRANCH_FACTOR)
        table_keys = self.table.keys()

        for idx in rand_idxs:
            title = table_keys[idx]
            self.page = wikipage.get_wikipedia_page_from_title(title)
            self._save_outgoing_connections()

        maxLinks, maxTitle = None, None     
        for subject in self.table.keys():
            if (maxLinks is None or self.table.hits(subject) > maxLinks) \
                and (subject not in self.trace):
                maxLinks = self.table.hits(subject)
                maxTitle = subject

        self.subject = maxTitle
        self.page = wikipage.get_wikipedia_page_from_title(maxTitle)

        print(f"{self.trace} -> {self.subject}")

        self.trace.append(self.subject)
    
    def most_popular_pathway(self):
        most_popular = self.most_popular()
        return self.table.unravel(most_popular)

    def most_popular(self):
        popularPage = None
        mostViews = -1

        for page in self.trace:
            views = get_page_views(page,
                                 constants.PAGEVIEWS_QUERY_START,
                                 constants.PAGEVIEWS_QUERY_END,
                                 constants.PAGEVIEWS_QUERY_GRANULARITY)[0]
            if views > mostViews:
                popularPage = page
                mostViews = views

        return popularPage

    def _save_outgoing_connections(self):
        for link in wikipage.get_outgoing_links(self.page):
            if 'identifier' in link.title():
                    continue
            self.table.spot(link.title(), self.subject)

