import os
import yaml

# general constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.yaml')

# Load in config.yaml
with open(CONFIG_PATH, "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

# pageviews.py constants
PAGEVIEWS_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
PAGEVIEWS_WEBSITE = config["PERSONAL_WEBSITE"]
PAGEVIEWS_EMAIL_ADDRESS = config["EMAIL_ADDRESS"]

# word2vec.py constants
W2V_PRETRAINED_MODEL = "fasttext-wiki-news-subwords-300"
W2V_GENSIM_PATH = os.path.join(DATA_DIR, "w2v")
W2V_KEY_LIMIT = 200000