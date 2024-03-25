import os
import yaml
from datetime import datetime

# General constants.
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.yaml')

# Load configurations.
with open(CONFIG_PATH, "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

# Pageviews API constants
PAGEVIEWS_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
PAGEVIEWS_WEBSITE = config["PERSONAL_WEBSITE"]
PAGEVIEWS_EMAIL_ADDRESS = config["EMAIL_ADDRESS"]
PAGEVIEWS_QUERY_START = datetime(2020, 10, 1, 0)
PAGEVIEWS_QUERY_END = datetime(2020, 11, 1, 0)
PAGEVIEWS_QUERY_GRANULARITY = 'MONTHLY'

# Title2Vec constants
T2V_PRETRAINED_MODEL = "fasttext-wiki-news-subwords-300"
T2V_GENSIM_PATH = os.path.join(DATA_DIR, "w2v")
T2V_NLTK_PATH = os.path.join(DATA_DIR, "nltk")
T2V_KEY_LIMIT = 200000

# Similar Traversal Constants
SIM_PRIORITYQUEUE_SIZE = 10

# Popular constants
POP_EXPLORE_PER_TRAVERSAL = 5
