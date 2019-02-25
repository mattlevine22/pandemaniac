import networkx as nx
import sim
import json
import numpy as np
from math import floor

def graph_from_string(string):
	data = json.loads(string,
		object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})

	data = {str(k): [str(u) for u in v] for k, v in data.items() if len(v)>0}
	return dict2graph(data), data

def graph_from_file(file_name):
	"""Read in graph from json file

	INPUT: file_name pointing to a JSON file
	OUTPUT: dictionary with integer nodes as keys and values
	"""
	# read in JSON file to a dictionary with integer valued nodes
	with open(file_name, "r") as content:
		data = json.load(content,
			object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
	# remove disconnected nodes (i.e. len(v)>0)
	# convert to integers
	data = {k: [int(u) for u in v] for k, v in data.items() if len(v)>0}
	return data, dict2graph(data)

def dict2graph(my_dict):
	"""Convert dictionary of nodes-edges to networkx graph object"""
	# initialize graph object
	graph = nx.Graph()
	# add all nodes
	graph.add_nodes_from(my_dict.keys())
	# add all edges
	for node in my_dict:
		graph.add_edges_from([(node,k) for k in my_dict[node]])
	return graph


# NOTE: metrics to look at:
# current_flow_closeness_centrality
# percolation_centrality

# if __name__ == "__main__":
# 	choose strategies
# 	file_name = 'testgraph1.json'
# 	data, graph = graph_from_file(file_name)
# 	n_nodes = int(len(graph.nodes)/4)
# 	nodes = {}
# 	nodes["strategy1"] = choose_random_nodes(graph=graph, n_nodes=n_nodes)
# 	nodes["strategy2"] = choose_highest_degree_nodes(graph=graph, n_nodes=n_nodes)
# 	nodes["strategy3"] = choose_highest_closeness_centrality_nodes(graph=graph, n_nodes=n_nodes)
# 	print(sim.run(data, nodes))
#
#
# 	choose strategies
# 	file_name = 'testgraph2.json'
# 	data, graph = graph_from_file(file_name)
# 	n_nodes = int(len(graph.nodes)/4)
# 	nodes = {}
# 	nodes["strategy1"] = choose_random_nodes(graph=graph, n_nodes=n_nodes)
# 	nodes["strategy2"] = choose_highest_degree_nodes(graph=graph, n_nodes=n_nodes)
# 	nodes["strategy3"] = choose_highest_closeness_centrality_nodes(graph=graph, n_nodes=n_nodes)
# 	print(sim.run(data, nodes))
