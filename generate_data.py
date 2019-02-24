import numpy as np
import matplotlib.pyplot as plt

from strategies import *
from generate import *
from sim import run

data_file = open("data/test.txt", "w")

def winner(result):
	return max(result.keys(), key=lambda x: result[x])

def run_games(graph_generator, game_strategies, n_seeds, n_games):
	results = {strat : 0 for strat in game_strategies}
	for _ in range(n_games):
		graph_nx, graph_dict = graph_generator()
		game_result = run_single_game(graph_nx, graph_dict, game_strategies, n_seeds)
		results[winner(game_result)] += 1

	return {strat : score / n_games for strat, score in results.items()}

def run_single_game(graph_nx, graph_dict, game_strategies, n_seeds):
	seeds = {}
	for strat in game_strategies:
		seeds[strat] = game_strategies[strat](graph_nx, n_seeds)

	return run(graph_dict, seeds) # {'strategy2': 473, 'strategy3': 24}


strategies = {
	"0" : highest_degree,
	"1" : highest_closeness_centrality
}

output_grid = np.zeros((10, 10, 2))
intput_grid = np.zeros([10, 10, 2])
for n_nodes, i in zip(range(100, 200, 10), range(10)):
	for n_seeds, j in zip(range(10, 20), range(10)):
		graph_generator = lambda : generate_graph("watts_strogatz", [n_nodes, n_seeds, .1])
		results = run_games(graph_generator, strategies, n_seeds, 20)
		print(results)

		intput_grid[i][j] = np.array([n_nodes, n_seeds])
		output_grid[i][j] = np.array([results['0'], results['1']])
		print("{},{}\t{}".format(n_nodes, n_seeds, winner(results)), file=data_file)

data_file.close()

plt.pcolormesh(output_grid[:, :, 0])
plt.show()


# data_set = {}
# for graph_size in [1000,10000,100000]:
# 	for gen_func in list_of_generator_functions:
# 		for k in range(N_graphs):
# 		# choose a generator function parameters at random
# 		# DO THIS
# 		gen_params = gen_param_dict[gen_func]
# 		graph_nx, graph_dict = generate_graph(gen_func, gen_params)
# 		for n_players in [2,3]:
# 			foo = [list(i) for i in itertools.product(BIG_strategy_list, repeat=n_players)]
# 			for n_seeds in (graph_size/n_players)*[1.5, 1, 0.5]:
# 				n_seeds = floor(n_seeds)
# 				for list_of_strats in foo:
# 					my_results = run_game(graph_nx, graph_dict, list_of_strats, n_seeds)
# 					ouptut.append({'graph_size': graph_size,
# 									'gen_func': gen_func,
# 									'k': k,
# 									'n_players': n_players,
# 									'n_seeds': n_seeds,
# 									'list_of_strats': list_of_strats,
# 									'my_results': my_results})
