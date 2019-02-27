from sys import exit
from time import time, sleep
import requests
import mechanize

GRAPH_FILE = "graphs/graph_{}.json"

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



if __name__ == "__main__":
    graph_label = "8.35.1"
    # n_players, n_seeds, graph_id = [int(val) for val in graph_label.split(".")]
    # seeds_file = "seeds.txt"
    # with open(seeds_file, 'w') as f:
    #     for i in range(50 * n_seeds):
    #         f.write("1\n".format(i))
    # #
    # # start = time()
    # # b = logged_in_browser()
    download(graph_label=graph_label)
    # upload(seeds_file=seeds_file, graph_label=graph_label)
    # print("time:", time() - start)
