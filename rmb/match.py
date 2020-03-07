from networkx.algorithms.matching import max_weight_matching
import matplotlib.pyplot as plt
import networkx as nx
from time import time
from collections import defaultdict
from pprint import pprint

# G = nx.complete_graph(32)
# G = nx.cycle_graph(32)
# G = nx.star_graph(32)
# G = nx.path_graph(32)

# s = max_weight_matching(G)
# print(len(s), s, len(s))
# nx.draw(G)
# plt.show()

# outer: graph's type & params
# inner: # of nodes
stats = defaultdict(lambda: defaultdict(lambda: []))
avg_stats = defaultdict(lambda: [])

# graph_type = [nx.star_graph, nx.path_graph,
#               nx.cycle_graph, nx.complete_graph,
#               nx.erdos_renyi_graph,
#               nx.newman_watts_strogatz_graph,
#               nx.random_geometric_graph]
# nodes_range = list(range(4, 32 + 1, 4))

graph_type = [nx.complete_graph,
              nx.erdos_renyi_graph,
              nx.random_geometric_graph]
nodes_range = [128, 256, 512, 1024]
# gnp_p = [0.3, 0.5, 0.9]  # required by nx.erdos_renyi_graph, nx.newman_watts_strogatz_graph
gnp_p = [0.9]  # required by nx.erdos_renyi_graph, nx.newman_watts_strogatz_graph
# new_k = [0.3, 0.5, 0.9]  # required by nx.newman_watts_strogatz_graph
# ran_r = [0.3, 0.5, 0.9]  # required by nx.random_geometric_graph
ran_r = [0.9]  # required by nx.random_geometric_graph


def time_maximum_matching(G):
    time1 = time()
    s = max_weight_matching(G)
    time2 = time()
    return len(s), time2 - time1


def time_it_loop():
    for g_type in graph_type:
        if g_type == nx.erdos_renyi_graph:
            for n in nodes_range:
                for p in gnp_p:
                    G = g_type(n, p)
                    name = f"{repr(g_type).split()[1]}(p={p})"
                    l, t = time_maximum_matching(G)
                    stats[name][n].append(t)

        # elif g_type == nx.newman_watts_strogatz_graph:
        #     for n in nodes_range:
        #         for k in new_k:
        #             for p in gnp_p:
        #                 G = g_type(n, int(n * k), p)
        #                 name = f"{repr(g_type).split()[1]}(k={k}, p={p})"
        #                 l, t = time_maximum_matching(G)
        #                 stats[name][n].append(t)
        elif g_type == nx.random_geometric_graph:
            for n in nodes_range:
                for r in ran_r:
                    G = g_type(n, r)
                    name = f"{repr(g_type).split()[1]}(r={r})"
                    l, t = time_maximum_matching(G)
                    stats[name][n].append(t)
        else:
            for n in nodes_range:
                G = g_type(n)
                name = f"{repr(g_type).split()[1]}"
                l, t = time_maximum_matching(G)
                stats[name][n].append(t)


if __name__ == '__main__':
    for i in range(10):
        time_it_loop()
    for name in stats:
        for n in nodes_range:
            avg = sum(stats[name][n]) / len(stats[name][n])
            avg_stats[name].append(avg)
    pprint(avg_stats)
    # print(nodes_range)
