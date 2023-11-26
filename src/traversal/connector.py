from traversal.popular import PopularTraversal
from traversal.similar import SimilarTraversal
from traversal.table import WikipageTable

def connect(start_subject, end_subject):
    print("Starting Kickoff Popularity Traversal...")
    start_pt = PopularTraversal(start_subject)
    for _ in range(5):
        start_pt.traverse()

    start_pathway = start_pt.most_popular_pathway()

    print("Starting Destination Popularity Traversal...")
    end_pt = PopularTraversal(end_subject)
    for _ in range(5):
        end_pt.traverse()

    end_pathway = end_pt.most_popular_pathway()

    popular_start = start_pathway[-1]
    popular_end = end_pathway[-1]

    print("Starting Similarity Traversal...")
    st = SimilarTraversal(popular_start, popular_end)
    
    while not st.found():
        st.safe_traversal()

    final_pathway = start_pathway[:-1] + st.table.unravel(popular_end) + end_pathway[1::-1]
    
    print("PATHWAY: ", final_pathway)
    
    
        