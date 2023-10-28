import constants
import gensim.downloader as api
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import nltk
import os
import numpy as np
import string

class VectorizedTitle(object):
    def __init__(self):
        self.vectors = list()
        self.tokens = list()
        self.size = 0

    def add(self, token, vector):
        self.tokens.append(token)
        self.vectors.append(vector)
        self.size += 1

    def get_vectors(self):
        return np.array(self.vectors)
    
    def get_tokens(self):
        return self.tokens
    
    def __len__(self):
        return self.size


class Title2Vec(object):
    def __init__(self):
        self.stopwords = None
        self.embedder = None

        self._download_w2v()
        self._download_nltk()

    def title_to_vector(self, title: str):
        tokens = Title2Vec._tokenize_string(title)
        tokens = self._remove_stopwords(tokens)

        vectors = self.embedder.vectors_for_all(tokens)

        vectorized = VectorizedTitle()
        for token in tokens:
            if vectors.has_index_for(token):
                vectorized.add(token, vectors[token])
        
        return vectorized

    def word_to_vector(self, word: str):
        try:
            return self.embedder.get_vector(word.lower())
        except KeyError:
            return np.empty()

    def _remove_stopwords(self, tokens: list):
        return [token for token in tokens if not token in self.stopwords]

    @staticmethod
    def _tokenize_string(s: str, lower=True):
        tokens = nltk.tokenize.word_tokenize(s)
        tokens = [t for t in tokens if t[0] not in string.punctuation]
        if lower:
            tokens = [t.lower() for t in tokens]
        return tokens

    def _download_w2v(self):
        # Ensure directory for holding pretrained model exists
        if not os.path.isdir(constants.T2V_GENSIM_PATH):
            os.makedirs(constants.T2V_GENSIM_PATH)

        # Download model if missing
        if constants.T2V_PRETRAINED_MODEL not in os.listdir(constants.T2V_GENSIM_PATH):
            print("Word2Vec: Downloading pretrained weights...")
            path = api.load(constants.T2V_PRETRAINED_MODEL, return_path=True)
            print(f"Downloaded weights to:\n{path}")

        pretrained_path = os.path.join(constants.T2V_GENSIM_PATH, constants.T2V_PRETRAINED_MODEL)
        pretrained_path = os.path.join(pretrained_path, f"{constants.T2V_PRETRAINED_MODEL}.gz")
        self.embedder = KeyedVectors.load_word2vec_format(pretrained_path, 
                                                       binary=False, 
                                                       limit=constants.T2V_KEY_LIMIT)

    def _download_nltk(self):
        # Ensure directory for holding nltk stopwords exists
        if not os.path.isdir(constants.T2V_NLTK_PATH):
            os.makedirs(constants.T2V_NLTK_PATH)

        # Download stopwords if missing
        if 'corpora' not in os.listdir(constants.T2V_NLTK_PATH):
            print("Word2Vec: Downloading nltk stopwords...")
            nltk.download('stopwords', download_dir=constants.T2V_NLTK_PATH)
            print("Downloaded nltk.stopwords")
        
        # Download punkt if missing
        if 'tokenizers' not in os.listdir(constants.T2V_NLTK_PATH):
            print("Word2Vec: Downloading nltk punkt...")
            nltk.download('punkt', download_dir=constants.T2V_NLTK_PATH)
            print("Downloaded ntlk.punkt")

        nltk.data.path.append(constants.T2V_NLTK_PATH)
        self.stopwords = set(stopwords.words("english"))
