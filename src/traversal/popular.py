from api import wikipage
from score.popular import outgoing_links

class PopularTraversal(object):
    def __init__(self, start_subject):
        self.subject = start_subject
        self.trace = [start_subject]

        self.page = wikipage.get_wikipedia_page_from_title(start_subject) 

    def traverse(self):
        topScore = -1
        topPage = None

        for i, link in enumerate(wikipage.get_outgoing_links(self.page)):
            print(i)
            ol = outgoing_links(link)
            if ol > topScore:
                topScore = ol
                topPage = link

        self.page = topPage
        self.subject = topPage.title()
        self.trace.append(self.subject)