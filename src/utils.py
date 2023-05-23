import random
from collections import deque

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

BUNDESTAG_DATA_PATH = "data/Bundestag/"
BUNDESTAG_GRAPH_PATH = "graphs/Bundestag/"
YEAR_TO_LEG_ID = {"2021": 132, "2017": 111, "2013": 97, "2009": 83, "2005": 67}


def year_to_period(year):
    return f'{year}-{int(year) + 4}'


def get_weight_list(G):
    weight_list = []
    for i, j in G.edges():
        weight_list.append(G[i][j]['weight'])
    return weight_list


def get_hist_bin():
    return np.arange(0, 1.1, 0.1)


def plot_weights_hist(G, amount_bins=25):
    weights = get_weight_list(G)
    counts, hist = np.histogram(weights, bins=amount_bins)
    plt.hist(hist[:-1], bins=amount_bins,weights=counts/np.sum(counts) , edgecolor='black')
    plt.show()


# Needs the year as input
def read_graph(year: int):
    G = nx.read_pajek(BUNDESTAG_GRAPH_PATH + year_to_period(year) + "/network" + year_to_period(year) + ".net")
    G = nx.convert_node_labels_to_integers(G, label_attribute='label')
    return G


def component(G, N, i):
    C = []
    S = []
    N.remove(i)
    S.append(i)
    while S:
        i = S.pop()
        C.append(i)
        for j in G[i]:
            if j in N:
                N.remove(j)
                S.append(j)
    return C


def components(G):
    C = []
    N = set(G.nodes())
    while N:
        C.append(component(G, N, next(iter(N))))
    return C


def distance(G, i):
    D = [-1] * len(G)  # D = {}
    Q = deque()
    D[i] = 0
    Q.append(i)
    while Q:
        i = Q.popleft()
        for j in G[i]:
            if D[j] == -1:  # if j not in D:
                D[j] = D[i] + 1
                Q.append(j)
    return [d for d in D if d > 0]


def distances(G, n=100):
    D = []  # D = {}
    for i in G.nodes() if len(G) <= n else random.sample(G.nodes(), n):
        D.append(distance(G, i))  # D[i] = distance(G, i)
    return D


def isolated(G, i):
    for j in G[i]:
        if j != i:
            return False
    return True


def tops(G, C, centrality, n=15):
    print("{:>12s} | '{:s}'".format('Centrality', centrality))
    for i, c in sorted(C.items(), key=lambda item: (item[1], G.degree[item[0]]), reverse=True)[:n]:
        print("{:>12.6f} | '{:s}' ({:,d})".format(c, G.nodes[i]['label'], G.degree[i]))
    print()


def info(G):
    print("{:>10s} | '{:s}'".format('Graph', G.name))

    n = G.number_of_nodes()
    n0, n1, delta = 0, 0, 0
    for i in G.nodes():
        if isolated(G, i):
            n0 += 1
        elif G.degree(i) == 1:
            n1 += 1
        if G.degree(i) > delta:
            delta = G.degree(i)

    print("{:>10s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))

    m = G.number_of_edges()
    m0 = nx.number_of_selfloops(G)

    print("{:>10s} | {:,d} ({:,d})".format('Edges', m, m0))
    print("{:>10s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))

    C = components(G)

    print("{:>10s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))

    D = distances(G)
    D = [i for d in D for i in d]

    print("{:>10s} | {:.2f} ({:,d})".format('Distance', sum(D) / len(D), max(D)))

    if isinstance(G, nx.MultiGraph):
        G = nx.Graph(G)

    print("{:>10s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
    print()
    tops(G, {i: k / (len(G) - 1) for i, k in G.degree()}, 'degree')

    tops(G, nx.clustering(G), 'clustering')
    tops(G, {i: c * (G.degree(i) - 1) for i, c in nx.clustering(G).items()}, '~μ-clustering')
    tops(G, nx.eigenvector_centrality_numpy(G), 'eigenvector')

    tops(G, nx.pagerank(G), 'pagerank')

    tops(G, nx.closeness_centrality(G), 'closeness')

    tops(G, nx.betweenness_centrality(G), 'betweenness')


def createNXGraph(leg_year, base_path=BUNDESTAG_GRAPH_PATH):
    G = nx.Graph()
    leg_period = year_to_period(leg_year)
    filename_stem = "network" + leg_period
    with open(base_path + leg_period + '/' + filename_stem + '.net', 'r') as file:
        file.readline()

        for line in file:
            if line.startswith("*"):
                break
            else:
                node = line.strip(' ')
                node = node.split("\"")
                G.add_node(int(node[0]) - 1, label=node[1], cluster=node[3])

        for line in file:
            i, j, v = line.split()
            G.add_edge(int(i) - 1, int(j) - 1, weight=float(v))
    return G


def cluster_distances(G):
    cluster = {}
    for u, v, data in G.edges(data=True):

        cluster_tuple = (G.nodes[u]['cluster'], G.nodes[v]['cluster'])
        weight = data['weight']
        if cluster_tuple in cluster:
            current = cluster[cluster_tuple]
            cluster.update({cluster_tuple: (weight + current[0], 1 + current[1])})
        elif (cluster_tuple[1], cluster_tuple[0]) in cluster:
            current = cluster[(cluster_tuple[1], cluster_tuple[0])]
            cluster.update({(cluster_tuple[1], cluster_tuple[0]): (weight + current[0], 1 + current[1])})
        else:
            cluster.update({cluster_tuple: (weight, 1)})
    for c in cluster:
        print(c, cluster[c][0] / cluster[c][1])


G = createNXGraph(2013, './graphs/Bundestag/')
# cluster_distances(G)
# print(get_weight_list(G))
