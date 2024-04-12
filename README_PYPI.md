# Wiki Wormhole
## Description
This python library leverages graphs and artificial intelligence to find the path from a start wikipedia page to a destination wikipedia page.

## Installation
Install wikiwormhole through pip package manager.
```
pip install wikiwormhole
```
Then run the setup script to accomplish the following:
- Generate `config.yaml` script for the pageviews api (How many pageviews does a wikipedia page have).
- Download pre-trained Word2Vec model using Gensim.
- Download corpus of stop words (insignificant words) to help embed titles using natural language toolkit (NLTK).
```
python <venv-name>/bin/setup_wormhole.py <config-path> <download-path>
```
Here config path is where the new `config-yaml` will be created. The download path is where the Word2Vec model weights and NLTK corpus will be downloaded on your system.

The final step in installation is providing a personal website and email in the `config.yaml` file. Once filled you'll be able to use the pageviews API.

## Algorithm
The algorithm is split into two parts: popular and similar traversal.

**Popular Traversal** is an algorithm that attempts to find a more popular page connected to the original page.
In the small-world phenomenon it's observed its much easier to connect two separate "hubs" rather than two obscure nodes. The purpose of this algorithm is to find those popular hubs.

**Similar Traversal** is an algorithm that attempts to find the path of pages from the starting page to the destination page. The algorithm assumes that titles with similar words will be closer to each other in the graph than the contrary. This similarity calculation is powered by the infamous word embedder `Word2Vec`. The word embedder calculates the words position in a latent space and the similarity is then calculated for two separate words using a cosine similarity metric (emphasis on directional alignment rather than distance). 

### Sample Usage
.. code-block:: python
    from wikiwormhole.traverse.popular import PopularTraverse
    from wikiwormhole.traverse.similar import SimilarTraverse
    from wikiwormhole.title2vec import Title2Vec
    from tqdm import tqdm

    data_dir = './data'
    config_path = './config.yaml'

    start_title = 'Apple'
    end_title= 'Cadillac'

    pop_rounds = 5

    pop_start = PopularTraverse(start_title, config_path)
    pop_end = PopularTraverse(end_title, config_path)

    for _ in tqdm(range(pop_rounds)):
        pop_start.traverse()
        pop_end.traverse()

    path_start = pop_start.most_popular_pathway()
    path_end = pop_end.most_popular_pathway()
    print("START: ", path_start)
    print("END: ", path_end)

    t2v = Title2Vec(data_dir)
    sim_start, sim_end = path_start[-1], path_end[-1]
    sim_trav = SimilarTraverse(sim_start, sim_end, t2v)

    while not sim_trav.target_reached():
        sim_trav.traverse()

    path_cnx = sim_trav.path_to_target()
    print("RESULT: ", path_start[:-1] + path_cnx + path_end[:-1][::-1])