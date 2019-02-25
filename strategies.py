import numpy as np
import networkx as nx

def highest_degree(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(graph.degree, key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def random(graph, n):
    return [str(i) for i in np.random.choice(graph.nodes, size=n, replace=False)]

def highest_closeness_centrality(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.closeness_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def highest_katz_centrality_np(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.katz_centrality_numpy(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def highest_information_centrality(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.information_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def highest_subgraph_centrality(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.subgraph_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def highest_generalized_degree(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.generalized_degree(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def highest_second_order_centrality(graph, n, aug_frac=1.3):
    seeds = [str(k[0]) for k in sorted(nx.second_order_centrality(graph).items(), key=lambda x: x[1], reverse=True)]
    return np.random.choice(seeds[:(aug_frac*n)], n)

def target_cliques_v1(graph, n):
    """The idea is to request all nodes in the biggest cliques"""
    cliques = list(nx.find_cliques(graph))
    clique_sizes = [len(x) for x in cliques]
    my_seeds = set()
    for sz in reversed(range(max(clique_sizes))):
        big_cliques = [cli for cli in cliques if len(cli)==sz]
        for cli in big_cliques:
            for seed in cli:
                my_seeds.add(str(seed))
                if len(my_seeds) == n:
                    return my_seeds

def target_cliques_v2(graph, n, frac=0.7):
    """The idea is to request a FRACTION of nodes in the biggest cliques"""
    cliques = list(nx.find_cliques(graph))
    clique_sizes = [len(x) for x in cliques]
    my_seeds = set()
    for sz in reversed(range(max(clique_sizes))):
        big_cliques = [cli for cli in cliques if len(cli)==sz]
        for cli in big_cliques:
            random_seeds = np.random.choice(cli, ceil(frac*sz))
            for seed in random_seeds:
                my_seeds.add(str(seed))
                if len(my_seeds) == n:
                    return my_seeds


strategies_master_list = [
    highest_degree,
    random,
    highest_closeness_centrality,
    highest_katz_centrality_np,
    highest_information_centrality,
    target_cliques_v2,
    target_cliques_v1
]
