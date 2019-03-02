import numpy as np
import networkx as nx

# TODO: strategy class?
AUG_FRAC = 1.5

def greedy_maxCover_without_highest_degree(graph, n):
    high_seeds = set(highest_degree(graph, n))
    greedy_seeds = greedy_maxCover(graph, 2 * n)

    output = []
    for s in greedy_seeds:
        if s not in high_seeds:
            output.append(s)

    return output[:n]

def greedy_maxCover_without_k_highest_degree(graph, n, k=1):
    high_seeds = set(highest_degree(graph, k))
    greedy_seeds = greedy_maxCover(graph, n+k)

    output = []
    for s in greedy_seeds:
        if s not in high_seeds:
            output.append(s)

    return output[:n]

def greedy_maxCover_without_1_highest_degree(graph, n):
    return greedy_maxCover_without_k_highest_degree(graph, n, k=1)

def greedy_maxCover_without_quarter_highest_degree(graph, n):
    return greedy_maxCover_without_k_highest_degree(graph, n, k=int(0.25*n))

def greedy_maxCover_without_half_highest_degree(graph, n):
    return greedy_maxCover_without_k_highest_degree(graph, n, k=int(0.5*n))

def greedy_maxCover_without_threequarters_highest_degree(graph, n):
    return greedy_maxCover_without_k_highest_degree(graph, n, k=int(0.75*n))

def greedy_maxCover_without_all_highest_degree(graph, n):
    return greedy_maxCover_without_k_highest_degree(graph, n, k=n)


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

def highest_closeness_vitality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.closeness_vitality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_betweenness_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.betweenness_centrality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_load_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.load_centrality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_approximate_current_flow_betweenness_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    CC = max(nx.connected_component_subgraphs(graph), key=len)
    seeds = [str(k[0]) for k in sorted(nx.approximate_current_flow_betweenness_centrality(CC).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_current_flow_betweenness_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    CC = max(nx.connected_component_subgraphs(graph), key=len)
    seeds = [str(k[0]) for k in sorted(nx.current_flow_betweenness_centrality(CC).items(), key=lambda x: x[1], reverse=True)]

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

def highest_pagerank(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.pagerank(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def highest_eigenvector_centrality(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    seeds = [str(k[0]) for k in sorted(nx.eigenvector_centrality(graph).items(), key=lambda x: x[1], reverse=True)]

    if deterministic:
        return seeds[:n]
    return list(np.random.choice(seeds[:int(aug_frac * n)], n, replace=False))

def greedy_maxCover(graph, n, aug_frac=AUG_FRAC, deterministic=True):
    my_seeds = set()
    covered_nodes = set()
    node_sets = {node : set(graph.neighbors(node)) for node in graph.nodes}

    while len(my_seeds) < n:
        for node in graph.nodes:
            node_sets[node] -= covered_nodes
        best_node = max(graph.nodes, key=lambda v: len(node_sets[v]))
        my_seeds.add(best_node)
        covered_nodes.add(best_node)
        covered_nodes.update(node_sets[best_node])

    return list(my_seeds)


def secure_single_highD_with_lowD_neighbors(graph, n, n_neighbors=2):
    # rank nodes by decreasing degree
    source_node = sorted(graph.degree, key=lambda x: x[1], reverse=True)[0][0]
    # rank neighbors by increasing degree
    my_seeds = [x[0] for x in sorted(graph.degree(graph.neighbors(source_node)), key=lambda x: x[1], reverse=False)[:(n-1)]]
    my_seeds.append(source_node)
    return [str(s) for s in my_seeds]


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

def ta_more(graph, n):
    return ["11", "193", "5", "201", "2", "93", "59", "58", "245", "6", "40", "213"]

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
            target_cliques_v2,
            secure_single_highD_with_lowD_neighbors,
            highest_pagerank,
            greedy_maxCover,
            highest_betweenness_centrality,
            highest_approximate_current_flow_betweenness_centrality,
            highest_load_centrality,
            highest_eigenvector_centrality,
            highest_closeness_vitality
        ]

    if scope == "team":
        return [
            # highest_degree, #did NOT beat TA_more
            # highest_closeness_centrality,
            # highest_katz_centrality_np, #did NOT beat TA_more
            # highest_information_centrality, #did NOT beat TA_more
            # highest_subgraph_centrality, #did NOT beat TA_more
            # swarm_high_degrees,
            # target_cliques_v1, #did NOT beat TA_more
            # target_cliques_v2, #did NOT beat TA_more
            # secure_single_highD_with_lowD_neighbors, #did NOT beat TA_more
            # highest_pagerank,
            # greedy_maxCover,
            greedy_maxCover_without_highest_degree
            # greedy_maxCover_without_1_highest_degree,
            # greedy_maxCover_without_quarter_highest_degree,
            # greedy_maxCover_without_half_highest_degree,
            # greedy_maxCover_without_threequarters_highest_degree,
            # greedy_maxCover_without_all_highest_degree
            # highest_betweenness_centrality,
            # highest_approximate_current_flow_betweenness_centrality,
            # highest_current_flow_betweenness_centrality,
            # highest_load_centrality,
            # highest_eigenvector_centrality, #did NOT beat TA_more
            # highest_closeness_vitality #VERY SLOW
        ]

    if scope == "opp":
        return [
            # highest_degree
            # ta_strat
            # ta_more
            random
            # highest_closeness_centrality,
            # highest_katz_centrality_np,
            # highest_information_centrality,
            # highest_subgraph_centrality,
            # highest_generalized_degree
            # highest_second_order_centrality,
            # target_cliques_v1
            # target_cliques_v2
        ]
