import constants
import gensim.downloader as api
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import os
import time

# Ensure directory for holding pretrained model exists
if not os.path.isdir(constants.W2V_GENSIM_PATH):
    os.makedirs(constants.W2V_GENSIM_PATH)

# Download model if missing
if constants.W2V_PRETRAINED_MODEL not in os.listdir(constants.W2V_GENSIM_PATH):
    print("Word2Vec: Downloading pretrained weights...")
    path = api.load(constants.W2V_PRETRAINED_MODEL, return_path=True)
    print(f"Downloaded weights to:\n{path}")

pretrained_path = os.path.join(constants.W2V_GENSIM_PATH, constants.W2V_PRETRAINED_MODEL)
pretrained_path = os.path.join(pretrained_path, f"{constants.W2V_PRETRAINED_MODEL}.gz")
model = KeyedVectors.load_word2vec_format(pretrained_path, binary=False, limit=constants.W2V_KEY_LIMIT)
print(model)
print("FINISHED")

# kv = model.vectors_for_all(["santa","christmas","apple"])
# for x in kv:
#   print(x)