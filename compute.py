from sys import exit
import os
from time import time
import struct
import json
import subprocess as sub
from multiprocessing import Pool
import itertools
from http.server import BaseHTTPRequestHandler, HTTPServer

from test_script1 import *
from sim import *
from strategies import *

HOST_NAME = 'localhost'
PORT_NUMBER = 6900
N_PROCS = 4

def run_game(args):
    graph_nx, graph_dict, team_seeds, opp_seeds = args
    # logs = open("logs/{}.txt".format(os.getpid()), "w")

    # team_seeds = [strat(graph_nx, n_seeds) for strat in team_strats]
    # opp_seeds = [strat(graph_nx, n_seeds) for strat in opp_strats]

    input_seeds = {
        "team" : team_seeds,
        "opp" : opp_seeds,
    }
    score = run(graph_dict, input_seeds)

    # logs.close()
    return score["team"] / len(graph_dict)


def simulate_strategies(graph_nx, graph_dict, n_players, n_seeds, team_strats, opp_strats):
    n, m = len(team_strats), len(opp_strats)
    team_seeds = [strat(graph_nx, n_seeds) for strat in team_strats]
    opp_seeds = [strat(graph_nx, n_seeds) for strat in opp_strats]

    args = []
    for i in range(n):
        for j in range(m):
            args.append((graph_nx, graph_dict, team_seeds[i], opp_seeds[j]))

    with Pool(N_PROCS) as pool:
        scores = pool.map(run_game, args)

    return np.array(scores).reshape((n, m))

def compute_seeds(graph_nx, graph_dict, n_players, n_seeds):
    team_strats = get_strats("team")
    opp_strats = get_strats("opp", n_players)

    scores = simulate_strategies(graph_nx, graph_dict, n_players, n_seeds, team_strats, opp_strats)
    strategy_scores = np.sum(scores, axis=1)
    winning_strat = team_strats[np.argmax(strategy_scores)]
    print(winning_strat)

    seeds = '\n'.join(winning_strat(graph_nx, n_seeds))
    return seeds


class ComputeHandler(BaseHTTPRequestHandler):
    # def do_HEAD(self):
    #     pass
        # print("do head")
        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()

    def do_POST(self):
        self.respond({'status': 200})

    def game_from_body(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))
        graph_nx, graph_dict = graph_from_string(body["graph"])
        n_players, n_seeds = int(body["n_players"]), int(body["n_seeds"])

        print("game specs:", len(graph_dict), n_players, n_seeds)
        return graph_nx, graph_dict, n_players, n_seeds

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        start = time()
        seeds = compute_seeds(*self.game_from_body())
        print("compute time:", time() - start)

        return seeds.encode("utf-8")

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ComputeHandler)
    print("server up: {}:{}".format(HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("server down")
