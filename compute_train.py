import os, sys
from time import time
import struct
import json
import subprocess as sub
from multiprocessing import Pool
import itertools
from http.server import BaseHTTPRequestHandler, HTTPServer

from load import *
from sim import *
from strategies import *

N_PROCS = 4

scoreboard = [20, 15, 12, 9, 6, 4, 2, 1, 0, 0]

def run_game(args):
    graph_nx, graph_dict, input_seeds = args
    # with open("logs/{}.txt".format(os.getpid()), 'a') as f:
    #     print(input_seeds, file=f)
    # logs = open("logs/{}.txt".format(os.getpid()), "w")

    # team_seeds = [strat(graph_nx, n_seeds) for strat in team_strats]
    # opp_seeds = [strat(graph_nx, n_seeds) for strat in opp_strats]

    return run(graph_dict, input_seeds)

    # logs.close()
    # NOTE: rint vs score


# def simulate_strategies(graph_nx, graph_dict, n_players, n_seeds, team_strats, opp_strats):
#     n, m = len(team_strats), len(opp_strats)
#     team_seeds = [strat(graph_nx, n_seeds) for strat in team_strats]
#     opp_seeds = [strat(graph_nx, n_seeds) for strat in opp_strats]
#
#     args = []
#     for i in range(n):
#         for j in range(m):
#             args.append((graph_nx, graph_dict, team_seeds[i], opp_seeds[j]))
#
#     with Pool(N_PROCS) as pool:
#         scores = pool.map(run_game, args)
#
#     return np.array(scores).reshape((n, m))

def make_seeds(args):
    strat, graph_nx, n_seeds = args
    return strat(graph_nx, n_seeds)

def train_strategies(graph_nx, graph_dict, n_players, n_seeds, game_data, n_mix_samples=10):
    # start timer
    start = time()
    team_strats = get_strats("team")

    with Pool(N_PROCS) as pool:
        team_seeds = pool.map(make_seeds, [(s, graph_nx, n_seeds) for s in team_strats])
    # print(game_data)
    all_teams = [team for team in game_data]

    n_strats = len(team_strats)
    n_rounds = len(game_data["Animaniacs"]) # always 50
    n_teams = len(all_teams)

    args = []
    for i in range(n_strats):
        for j in range(n_rounds):
            single_game_seeds = {team : seeds[j] for team, seeds in game_data.items()}
            single_game_seeds["Animaniacs"] = team_seeds[i]
            args.append((graph_nx, graph_dict, single_game_seeds))

    # mix up the seed nodes and see what falls out
    bag_of_seeds = list(set([item for sublist in team_seeds for item in sublist]))
    for i in range(n_mix_samples):
        for j in range(n_rounds):
            single_game_seeds = {team : seeds[j] for team, seeds in game_data.items()}
            single_game_seeds["Animaniacs"] = np.random.choice(bag_of_seeds, n_seeds, replace=False)
            args.append((graph_nx, graph_dict, single_game_seeds))

    with Pool(N_PROCS) as pool:
        scores = pool.map(run_game, args)

    strat_scores = {}
    all_strat_sums = {}
    strat_sums = {}
    team_wins = {}
    # for strat in team_strats:
    #     strat_scores[strat] = {team : 0 for team in game_data}
    # for i in range(n_strats):
    #     for j in range(n_rounds):
    #         winning_nm = max([nm for nm in scores[i*n_rounds + j]], key=lambda nm: scores[i*n_rounds + j][nm])
    #         team_wins[winning_nm] += 1
    for i in range(n_strats + n_mix_samples):
        foo = {team: 0 for team in all_teams}
        foo_wins = {team: 0 for team in all_teams}
        for j in range(n_rounds):
            winning_nm = max([nm for nm in scores[i*n_rounds + j]], key=lambda nm: scores[i*n_rounds + j][nm])
            foo_wins[winning_nm] += 1
            for k in range(n_teams):
                foo[all_teams[k]] += scores[i*n_rounds + j][all_teams[k]]

        rank = len([s for s in foo.values() if s > foo["Animaniacs"]])
        if i < n_strats:
            strat_nm = team_strats[i]
        else:
            strat_nm = "mix_{}".format(i-n_strats)
        strat_sums[strat_nm] = foo["Animaniacs"]
        strat_scores[strat_nm] = scoreboard[rank]
        team_wins[strat_nm] = foo_wins["Animaniacs"]
        all_strat_sums[strat_nm] = {team: foo[team] for team in all_teams}

    print("STRATEGY SCORES")
    cc = 0
    for strat in sorted([strat for strat in strat_scores], key=lambda s: (strat_scores[s], strat_sums[s]), reverse=True):
        print(strat, strat_sums[strat], team_wins[strat]/50, strat_scores[strat])
        cc += 1
        if cc > 30:
            break
        # print(all_strat_sums[strat])

    # strategy_scores = np.mean(scores, axis=1)
    # best_score = np.max(strategy_scores)
    # if best_score > 0.5:
    #     winning_strat = team_strats[np.argmax(strategy_scores)]
    # else:
    #     winning_strat = highest_degree
    # print(winning_strat)

    # print("best score:", best_score)
    print()
    print("compute time:", time() - start, '\n\n')

    return "fake plastic trees please"

# def compute_seeds(graph_nx, graph_dict, n_players, n_seeds):
#     start = time()
#
#     team_strats = get_strats("team")
#     opp_strats = get_strats("opp", n_players)
#
#     scores = simulate_strategies(graph_nx, graph_dict, n_players, n_seeds, team_strats, opp_strats)
#     strategy_scores = np.mean(scores, axis=1)
#     best_score = np.max(strategy_scores)
#     if best_score > 0.5:
#         winning_strat = team_strats[np.argmax(strategy_scores)]
#     else:
#         winning_strat = highest_degree
#     print(winning_strat)
#
#     print("best score:", best_score)
#     print("compute time:", time() - start, '\n\n')
#
#     seeds = '\n'.join(winning_strat(graph_nx, n_seeds)) + '\n'
#     return seeds


class ComputeHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.respond({'status': 200})

    def game_from_body(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))
        graph_nx, graph_dict = graph_from_string(body["graph"])
        n_players, n_seeds = int(body["n_players"]), int(body["n_seeds"])

        print("game specs:", len(graph_dict), n_players, n_seeds)
        return graph_nx, graph_dict, n_players, n_seeds

    def graph_and_game_data_from_body(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))
        graph_nx, graph_dict = graph_from_string(body["graph"])
        game_data = json.loads(body["game_data"])
        n_players, n_seeds = int(body["n_players"]), int(body["n_seeds"])

        print("game specs:", len(graph_dict), n_players, n_seeds)
        return graph_nx, graph_dict, n_players, n_seeds, game_data


    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        seeds = train_strategies(*self.graph_and_game_data_from_body())
        # seeds = compute_seeds(*self.game_from_body())

        return seeds.encode("utf-8")

if __name__ == '__main__':
    if sys.argv[1] == "local":
        HOST_NAME = "localhost"
    if sys.argv[1] == "remote":
        HOST_NAME = "pandemaniac"
    PORT_NUMBER = 6006

    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ComputeHandler)
    print("server up: {}:{}".format(HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("server down")
