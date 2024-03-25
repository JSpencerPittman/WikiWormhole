from src.traverse.popular import PopularTraverse
from src.traverse.similar import SimilarTraverse
from src.title2vec import Title2Vec

print("TEST: loading title2vec model")
t2v = Title2Vec()

print("TEST: Start Apple -> Car")
t1 = "Apple"
t2 = "Car"

print("TEST: Popular(Apple)")
start_pt = PopularTraverse(t1)

print("TEST: Popular(Car)")
end_pt = PopularTraverse(t2)

print("TEST: Similar(Apple,Car)")
sim = SimilarTraverse(t1, t2, t2v)
