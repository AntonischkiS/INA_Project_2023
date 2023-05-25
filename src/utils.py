import random
from collections import deque

import networkx as nx

BUNDESTAG_DATA_PATH = "data/Bundestag/"
BUNDESTAG_GRAPH_PATH = "graphs/Bundestag/"
YEAR_TO_LEG_ID = {"2021": 132, "2017": 111, "2013": 97, "2009": 83, "2005": 67}
ELEC_YEARS = [1949, 1953, 1957, 1961, 1965, 1969, 1972, 1976, 1980, 1983, 1987,
              1990, 1994, 1998, 2002, 2005, 2009, 2013, 2017, 2021, 2025]


def year_to_period(year):
    year = int(year)
    return f'{year}-{ELEC_YEARS[ELEC_YEARS.index(year)+1]}'


# Needs the year as input
def read_graph(year: int):
    G = nx.read_pajek(BUNDESTAG_GRAPH_PATH + year_to_period(year)+"/network"+year_to_period(year)+".net")
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


