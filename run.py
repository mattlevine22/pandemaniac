import sys
from time import time
import struct
import requests

GRAPH_FILE = "graphs/graph_{}.json"
SEEDS_FILE = "seeds/seeds_{}.txt"

LOGIN_URL = "http://35.167.100.168:3000/login"
DOWNLOAD_URL = "http://35.167.100.168:3000/submit/{}/download"

def download(game_name="2.5.1"):
    b = mechanize.Browser()
    b.set_handle_robots(False)

    b.open(login_url)
    b.select_form(action="/login")
    b.form["username"] = "Animaniacs"
    b.form["password"] = "2d82b0t8"
    b.submit()

    b.retrieve(download_url.format(game_name), GRAPH_FILE.format(game_name))


def compute_seeds(compute_url, game_name, n_players, n_seeds):
    result = requests.post(compute_url, json={
        "graph": open(GRAPH_FILE.format(game_name), 'r').read(),
        "n_players" : str(n_players),
        "n_seeds" : str(n_seeds)
    })

    print(result.content.decode("utf-8"))
    with open(SEEDS_FILE.format(game_name), 'w') as f:
        f.write(result.content.decode("utf-8") * 50)

if __name__ == "__main__":
    game_name = sys.argv[1]

    PORT = "6006"
    if sys.argv[2] == "local":
        COMPUTE_URL = "http://localhost:" + PORT + '/'
    if sys.argv[2] == "remote":
        COMPUTE_URL = "http://35.235.67.44:" + PORT + '/'

    download(game_name)

    n_players, n_seeds, graph_id = [int(val) for val in game_name.split(".")]
    compute_seeds(COMPUTE_URL, game_name, n_players, n_seeds)
