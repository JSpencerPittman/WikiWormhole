from traversal.popular import PopularTraversal
from traversal.similar import SimilarTraversal
from traversal.table import WikipageTable
import json


def connect(request):
    request = json.loads(request)

    start_subject = request['start']
    end_subject = request['end']
    popular_itr = request['popular']

    print("Starting Source Popularity Traversal...")
    start_pt = PopularTraversal(start_subject)
    for _ in range(popular_itr):
        start_pt.traverse()

    start_pathway = start_pt.most_popular_pathway()

    print("Starting Destination Popularity Traversal...")
    end_pt = PopularTraversal(end_subject)
    for _ in range(popular_itr):
        end_pt.traverse()

    end_pathway = end_pt.most_popular_pathway()

    popular_start = start_pathway[-1]
    popular_end = end_pathway[-1]

    print("Starting Similarity Traversal...")
    st = SimilarTraversal(popular_start, popular_end)

    while not st.found():
        st.safe_traversal()

    final_pathway = start_pathway[:-1] + \
        st.table.unravel(popular_end) + end_pathway[1::-1]

    results = dict(results=final_pathway)
    return json.dumps(results)
