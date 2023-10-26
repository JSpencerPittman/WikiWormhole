import os
import yaml

# config.yaml constants
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.yaml')

with open(CONFIG_PATH, "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

# pageviews.py constants
PAGEVIEWS_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
PAGEVIEWS_WEBSITE = config["PERSONAL_WEBSITE"]
PAGEVIEWS_EMAIL_ADDRESS = config["EMAIL_ADDRESS"]


if __name__ == "__main__":
    print(CONFIG_PATH)