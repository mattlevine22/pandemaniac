import sys
from time import time
import struct
import requests

from web import *

COMPUTE_URL = "http://localhost:6900"
GRAPH_FILE = "graph_{}.json"
SEEDS_FILE = "seeds_{}.txt"


def compute_seeds(game_name, n_players, n_seeds):
    result = requests.post(COMPUTE_URL, json={
        "graph": open(GRAPH_FILE.format(game_name), 'r').read(),
        "n_players" : str(n_players),
        "n_seeds" : str(n_seeds)
    })

    print(result.content.decode("utf-8"))
    with open(SEEDS_FILE.format(game_name), 'w') as f:
        f.write(result.content.decode("utf-8") * 50)

    # return result.content

if __name__ == "__main__":
    game_name = sys.argv[1]
    download(game_name)

    n_players, n_seeds, graph_id = [int(val) for val in game_name.split(".")]
    compute_seeds(game_name, n_players, n_seeds)
