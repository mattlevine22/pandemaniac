import sys
from time import time
import struct
import json
import requests
import mechanize

from strategies import *
from load import *

GRAPH_FILE = "graphs/graph_{}.json"
SEEDS_FILE = "seeds/seeds_{}.txt"
GAME_DATA_FILE = "game_data/game_data_{}.json"

LOGIN_URL = "http://35.167.100.168:3000/login"
SUBMIT_URL = "http://35.167.100.168:3000/submit/{}/download"
DOWNLOAD_URL = "http://35.167.100.168:3000/download/{}-Animaniacs.json"

def download(game_name="2.5.1"):
    b = mechanize.Browser()
    b.set_handle_robots(False)

    b.open(LOGIN_URL)
    b.select_form(action="/login")
    b.form["username"] = "Animaniacs"
    b.form["password"] = "2d82b0t8"
    b.submit()

    b.retrieve(SUBMIT_URL.format(game_name), GRAPH_FILE.format(game_name))

def download_game_data(game_name):
    b = mechanize.Browser()
    b.set_handle_robots(False)

    b.open(LOGIN_URL)
    b.select_form(action="/login")
    b.form["username"] = "Animaniacs"
    b.form["password"] = "2d82b0t8"
    b.submit()

    b.retrieve(DOWNLOAD_URL.format(game_name), GAME_DATA_FILE.format(game_name))

def find_unique_seeds(game_name, n_seeds):
    # graph_nx, graph_dict = graph_from_string()
    game_data = json.loads(open(GAME_DATA_FILE.format(game_name), 'r').read())

    for team in game_data:
        total_seeds = 0
        for i in range(50):
            team_seeds = set(game_data[team][i])

            for opp_team in game_data:
                if opp_team != team:
                    team_seeds -= set(game_data[opp_team][i])

            total_seeds += len(team_seeds)

        print(team, total_seeds / (50 * n_seeds))

def find_unique_seeds2(game_name, n_seeds):
    graph_nx, graph_dict = graph_from_string(open(GRAPH_FILE.format(game_name), 'r').read())
    game_data = json.loads(open(GAME_DATA_FILE.format(game_name), 'r').read())

    strategy = greedy_maxCover_without_highest_degree
    seeds = strategy(graph_nx, n_seeds)

    total_seeds = 0
    for i in range(50):
        team_seeds = set(seeds)

        for team in game_data:
            if team != "Animaniacs":
                team_seeds -= set(game_data[team][i])

        total_seeds += len(team_seeds)

    print(strategy, total_seeds / (50 * n_seeds))


if __name__ == "__main__":
    game_name = sys.argv[1]
    n_players, n_seeds, graph_id = [int(val) for val in game_name.split(".")]

    download(game_name)
    download_game_data(game_name)
    find_unique_seeds2(game_name, n_seeds)


    # train_best_strategy(COMPUTE_URL, game_name, n_players, n_seeds)
