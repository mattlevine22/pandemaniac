import numpy as np
import networkx as nx

# TODO: strategy class?
AUG_FRAC = 1.5

def random(graph, n):
    return [str(i) for i in np.random.choice(graph.nodes, size=n, replace=False)]

def highest_degree(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(graph.degree, key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_closeness_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.closeness_centrality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_katz_centrality_np(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.katz_centrality_numpy(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_information_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    CC = max(nx.connected_component_subgraphs(graph), key=len)
    seeds = [str(k[0]) for k in sorted(nx.information_centrality(CC).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_subgraph_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.subgraph_centrality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_generalized_degree(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    # TODO: some sort of error in this one
    seeds = [str(k[0]) for k in sorted(nx.generalized_degree(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_second_order_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    CC = max(nx.connected_component_subgraphs(graph), key=len)
    seeds = [str(k[0]) for k in sorted(nx.second_order_centrality(CC).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

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
            random_seeds = np.random.choice(cli, int(frac*sz), replace=False)
            for seed in random_seeds:
                my_seeds.add(str(seed))
                if len(my_seeds) == n:
                    return my_seeds

def swarm_high_degrees(graph, n, n_layers=1, n_neighbors=3):
    # rank nodes by degree
    ranked_nodes = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    my_seeds = set()
    for source, _ in ranked_nodes:
        my_seeds.add(source)
        # branch out from this central node 1 level
        goo = sorted(graph.degree(graph.neighbors(source)), key=lambda x: x[1], reverse=True)
        # new_nodes = list(np.random.choice(list(n_dist_nodes), n_neighbors, replace=False))
        for k in range(n_neighbors):
            # pdb.set_trace()
            my_seeds.add(goo[k][0])
            if len(my_seeds) == n:
                return [str(s) for s in my_seeds]

# def ta_strat(graph, n):
#     return ["49", "59", "57", "148", "135", "10", "107", "77"]

def ta_strat(graph, n):
    return highest_degree(graph, int(.8 * n))

def get_strats(scope, n_players=2):
    if scope == "master":
        return [
            highest_degree,
            random,
            highest_closeness_centrality,
            highest_katz_centrality_np,
            highest_information_centrality,
            highest_subgraph_centrality,
            highest_generalized_degree,
            highest_second_order_centrality,
            target_cliques_v1,
            target_cliques_v2
        ]

    if scope == "team":
        return [
            highest_degree,
            # random,
            highest_closeness_centrality,
            highest_katz_centrality_np,
            highest_information_centrality,
            highest_subgraph_centrality,
            swarm_high_degrees,
            # highest_generalized_degree
            highest_second_order_centrality,
            target_cliques_v1,
            target_cliques_v2
        ]

    if scope == "opp":
        return [
            highest_degree
            # ta_strat
            # random,
            # highest_closeness_centrality,
            # highest_katz_centrality_np,
            # highest_information_centrality,
            # highest_subgraph_centrality,
            # highest_generalized_degree
            # highest_second_order_centrality,
            # target_cliques_v1
            # target_cliques_v2
        ]
