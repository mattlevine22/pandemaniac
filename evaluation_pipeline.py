def choose_highest_degree_nodes(graph, n_seeds):
	foo = [k[0] for k in sorted(graph.degree, key=lambda x: x[1], reverse=True)]
	return foo[:n_seeds]


def run_game(graph_nx, graph_dict, list_of_strategies_functions, n_seeds):
	seeds = {}
	i = 0
	for strat in list_of_strategies_functions:
		seeds[i] = strat(graph_nx, n_seeds)
		i += 1
	game_results = sim.run(graph_dict, seeds) # {'strategy2': 473, 'strategy3': 24}
	return game_results

def generate_graph(gen_func, gen_params):
	graph_nx = gen_func(*gen_params)
	graph_dict = nx2dict(graph_nx)
	return graph_nx, graph_dict

BIG_strategy_list = [a,b,c,d,e]
output = []
for graph_size in [1000,10000,100000]:
	for gen_func in list_of_generator_functions:
		for k in range(N_graphs):
		# choose a generator function parameters at random
		# DO THIS
		gen_params = gen_param_dict[gen_func]
		graph_nx, graph_dict = generate_graph(gen_func, gen_params)
		for n_players in [2,3]:
			foo = [list(i) for i in itertools.product(BIG_strategy_list, repeat=n_players)]
			for n_seeds in (graph_size/n_players)*[1.5, 1, 0.5]:
				n_seeds = floor(n_seeds)
				for list_of_strats in foo:
					my_results = run_game(graph_nx, graph_dict, list_of_strats, n_seeds)
					ouptut.append({'graph_size': graph_size,
									'gen_func': gen_func,
									'k': k,
									'n_players': n_players,
									'n_seeds': n_seeds,
									'list_of_strats': list_of_strats,
									'my_results': my_results})
