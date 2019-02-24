import networkx as nx

gen_functions = {
    "gnp" : nx.gnp_random_graph,
    "fast_gnp" : nx.fast_gnp_random_graph,
    "erdos_renyi" : nx.erdos_renyi_graph,
    "binomial" : nx.binomial_graph,
    "newman_watts_strogatz" : nx.newman_watts_strogatz_graph,
    "watts_strogatz" : nx.watts_strogatz_graph
}

def generate_graph(gen_func, gen_params):
    graph_nx = gen_functions[gen_func](*gen_params)
    graph_dict_dict = nx.to_dict_of_dicts(graph_nx)
    graph_dict = {}
    for node, adjacencies in graph_dict_dict.items():
        graph_dict[str(node)] = [str(j) for j in adjacencies]

    return graph_nx, graph_dict
