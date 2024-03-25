import os

# General constants.
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

# Title2Vec constants
T2V_PRETRAINED_MODEL = "fasttext-wiki-news-subwords-300"
T2V_GENSIM_PATH = os.path.join(DATA_DIR, "w2v")
T2V_NLTK_PATH = os.path.join(DATA_DIR, "nltk")
T2V_KEY_LIMIT = 200000
