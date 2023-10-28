from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from embed.title2vec import VectorizedTitle

def title_similarity(title_vec1: VectorizedTitle,
                     title_vec2: VectorizedTitle):
    A = title_vec1.get_vectors()
    B = title_vec2.get_vectors()

    sim_mat = cosine_similarity_matrix(A, B)

    return sim_mat.max()

def cosine_similarity_matrix(A, B):
    dot = np.dot(A,B.T)
    
    A_norm = np.linalg.norm(A, axis=1)
    B_norm = np.linalg.norm(B, axis=1)

    A_norm = A_norm.reshape(-1, 1)
    B_norm = B_norm.reshape(1, -1)

    dot = dot / A_norm
    dot = dot / B_norm

    return dot