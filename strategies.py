import numpy as np
import networkx as nx

def highest_degree(graph, n):
    seeds = [str(k[0]) for k in sorted(graph.degree, key=lambda x: x[1], reverse=True)]
    return seeds[:n]

def random(graph, n):
    return [str(i) for i in np.random.choice(graph.nodes, size=n, replace=False)]

def highest_closeness_centrality(graph, n):
	seeds = [str(k[0]) for k in sorted(nx.closeness_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
	return seeds[:n]

def highest_percolation_centrality(graph, n):
    # NOTE: I tested this. This seems to be a legitimate bug on their end
    print(nx.percolation_centrality(graph))
    seeds = [str(k[0]) for k in sorted(nx.percolation_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
    print(seeds)
    return seeds[:n]

strategies_master_list = [
    highest_degree,
    random,
    highest_closeness_centrality,
    highest_percolation_centrality
]
