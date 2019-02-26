from time import time
import struct
import requests

from web import *

COMPUTE_URL = "http://localhost:6900"
GRAPH_FILE = "graph.json"
SEEDS_FILE = "seeds.txt"


def compute_seeds(graph_json, n_players, n_seeds):
    result = requests.post(COMPUTE_URL, json={
        "graph": graph_json,
        "n_players" : str(n_players),
        "n_seeds" : str(n_seeds)
    })

    print(result.content.decode("utf-8"))
    with open(SEEDS_FILE, 'w') as f:
        f.write(result.content.decode("utf-8"))

    # return result.content

if __name__ == "__main__":
    game = "2.5.1"
    download(game)

    n_players, n_seeds, graph_id = [int(val) for val in game.split(".")]
    compute_seeds(open(GRAPH_FILE, 'r').read(), n_players, n_seeds)
