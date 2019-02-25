from time import time
import requests

from web import *

server_url = "http://localhost:6900"

def compute_seeds(graph_json, n_players, n_seeds):
    response = requests.post(server_url, json={
        "graph": graph_json,
        "n_players" : str(n_players),
        "n_seeds" : str(n_seeds)
    })

    return response.content

if __name__ == "__main__":
    game = "2.5.1"
    n_players, n_seeds, graph_id = [int(val) for val in game.split(".")]
    download(game)

    seeds = compute_seeds(open("graph.json", 'r').read(), n_players, n_seeds)
    print(seeds)
    # with open("seeds.txt", 'w') as f:
    #     f.write(seeds)
