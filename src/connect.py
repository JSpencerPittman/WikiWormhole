from src.traverse.popular import PopularTraverse
from src.traverse.similar import SimilarTraverse


def connect(start_subject, end_subject):
    print("Starting Kickoff Popularity Traversal...")
    start_pt = PopularTraverse(start_subject)
    for _ in range(5):
        print("SubjectP1: ", start_pt._subject)
        start_pt.traverse()
    print("SubjectP1: ", start_pt._subject)

    start_pathway = start_pt.most_popular_pathway()

    print("Starting Destination Popularity Traversal...")
    end_pt = PopularTraverse(end_subject)
    for _ in range(5):
        print("SubjectP2: ", start_pt._subject)
        end_pt.traverse()
    print("SubjectP2: ", start_pt._subject)

    # end_pathway = end_pt.most_popular_pathway()

    # popular_start = start_pathway[-1]
    # popular_end = end_pathway[-1]

    # print("Starting Similarity Traversal...")
    # st = SimilarTraverse(popular_start, popular_end)

    # while not st.target_found():
    #     st.traverse()

    # final_pathway = start_pathway[:-1] + \
    #     st.table.unravel(popular_end) + end_pathway[1::-1]

    # print("PATHWAY: ", final_pathway)
