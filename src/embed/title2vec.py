import constants
import gensim.downloader as api
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import nltk
import os
import time

# Ensure directory for holding pretrained model exists
if not os.path.isdir(constants.T2V_GENSIM_PATH):
    os.makedirs(constants.T2V_GENSIM_PATH)

# Download model if missing
if constants.T2V_PRETRAINED_MODEL not in os.listdir(constants.T2V_GENSIM_PATH):
    print("Word2Vec: Downloading pretrained weights...")
    path = api.load(constants.T2V_PRETRAINED_MODEL, return_path=True)
    print(f"Downloaded weights to:\n{path}")

# Download stopwords if missing
if 'corpora' not in os.listdir(constants.T2V_NLTK_PATH):
    print("Word2Vec: Downloading nltk stopwords...")
    nltk.download('stopwords', download_dir=constants.T2V_NLTK_PATH)
    print("Downloaded stopwords")

nltk.data.append(constants.T2V_NLTK_PATH)
stop_words = set(stopwords.words("english"))



word = 'The santa claus'
# print(type(stopwords))

# pretrained_path = os.path.join(constants.T2V_GENSIM_PATH, constants.T2V_PRETRAINED_MODEL)
# pretrained_path = os.path.join(pretrained_path, f"{constants.T2V_PRETRAINED_MODEL}.gz")
# model = KeyedVectors.load_word2vec_format(pretrained_path, binary=False, limit=constants.T2V_KEY_LIMIT)
# print(model)
# print("FINISHED")

# kv = model.vectors_for_all(["santa","christmas","apple"])
# for x in kv:
#   print(x)