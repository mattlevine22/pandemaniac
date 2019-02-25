from sys import exit
import os
from time import time
import json
import subprocess as sub
from multiprocessing import Pool
import itertools
from http.server import BaseHTTPRequestHandler, HTTPServer

from test_script1 import *
from sim import *
from strategies import *

def winner(result):
	return max(result.keys(), key=lambda x: result[x])

def run_games(args):
    graph_nx, graph_dict, strat_indices, n_seeds, n_runs = args
    logs = open("logs/{}.txt".format(os.getpid()), "w")

    # print(graph_nx, graph_dict, game_strats, n_seeds, n_runs, file=logs)
    strategies = strategy_vector("test")

    scores = {str(i) : 0 for i in strat_indices}
    for _ in range(n_runs):
        seeds = {str(i) : strategies[i](graph_nx, n_seeds) for i in strat_indices}
        print(seeds, file=logs)
        print(graph_dict, file=logs)
        print(run(graph_dict, seeds), file=logs)

        for i, score in run(graph_dict, seeds).items():
            scores[i] += score

        print(scores, '\n', file=logs)

    logs.close()
    return scores

def compute_distributed(graph_nx, graph_dict, n_players, n_seeds, n_runs=10, n_procs=4):
    strategies = strategy_vector("test")
    strat_sets = list(itertools.product(range(len(strategies)), repeat=n_players))
    process_args = [(graph_nx, graph_dict, set, n_seeds, n_runs) for set in strat_sets]

    os.system("rm -r logs && mkdir logs")
    print(len(process_args))

    # print("nx", graph_nx)

    start = time()
    with Pool(n_procs) as pool:
        scores = pool.map(run_games, process_args)

    result = ""
    for score in scores:
        result += "{}\n".format(score)

    print("compute time:", time() - start)
    return result


class BasilHandler(BaseHTTPRequestHandler):
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

        return graph_nx, graph_dict, n_players, n_seeds

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        results = compute_distributed(*self.game_from_body())
        return bytes(results, 'UTF-8')

if __name__ == '__main__':
    HOST_NAME = 'localhost'
    PORT_NUMBER = 6900

    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), BasilHandler)
    print("server up: {}:{}".format(HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("server down")
