from tqdm import tqdm

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

BUNDESTAG_DATA_PATH = "data/Bundestag/"
BUNDESTAG_GRAPH_PATH = "graphs/Bundestag/"
BUNDESTAG_GRAPH_PATH_V2 = "graphs/Bundestag_only_Attendance/"
TRANSLATIONS = {"other": "fraktionslos", "Greens": "Die Grünen", "DIE GRÜNEN": "Die Grünen",
                "BÜNDNIS 90/DIE GRÜNEN": "Die Grünen",
                "Left/PDS": "Die Linke", "CDU/CSU": "CDU", "DIE LINKE.": "Die Linke", "DIE LINKE": "Die Linke"}
YEAR_TO_LEG_ID = {"2021": 132, "2017": 111, "2013": 97, "2009": 83, "2005": 67}
ELEC_YEARS = [1949, 1953, 1957, 1961, 1965, 1969, 1972, 1976, 1980, 1983, 1987,
              1990, 1994, 1998, 2002, 2005, 2009, 2013, 2017, 2021, 2025]


def translate_faction_name(name):
    if name in TRANSLATIONS:
        return TRANSLATIONS[name]
    return name


def sort_normalize_faction_name(c):
    old = c
    fst = translate_faction_name(c[0])  # translate to avoid duplicates
    snd = translate_faction_name(c[1])
    c = (max(fst, snd), min(fst, snd))  # sort tuple to avoid duplicates
    return c, old


def in_cluster_distance(year):
    G1 = createNXGraph(year, base_path=BUNDESTAG_GRAPH_PATH)
    G2 = createNXGraph(year, base_path=BUNDESTAG_GRAPH_PATH_V2)
    cluster1 = cluster_distances(G1)
    cluster2 = cluster_distances(G2)
    distances = []
    for c1 in cluster1:
        c1, old = sort_normalize_faction_name(c1)
        if c1[0] != c1[1] or c1[1] == 'fraktionslos' or c1[0] == 'fraktionslos':
            continue
        distances.append((c1[0], cluster1[old][0] / cluster1[old][1], cluster2[old][0] / cluster2[old][1]))
    return distances


def pairwise_cluster_distances(factions_to_eval=None):  # ["SPD", "CDU", "FDP"]
    faction_distance = {}
    years = {}
    for i, year in tqdm(enumerate(ELEC_YEARS[:-1])):
        G = createNXGraph(year, base_path=BUNDESTAG_GRAPH_PATH)
        cluster = cluster_distances(G)
        for c in cluster:
            c, old = sort_normalize_faction_name(c)
            # Exclude same faction and faction-less
            if c[0] == c[1] or c[1] == 'fraktionslos' or c[0] == 'fraktionslos':
                continue
            if factions_to_eval is not None:
                if c[0] not in factions_to_eval or c[1] not in factions_to_eval:
                    continue
            if c not in faction_distance:
                faction_distance[c] = []
            faction_distance[c].append(cluster[old][0] / cluster[old][1])
    for fc in faction_distance:
        years[fc] = [ELEC_YEARS[:-1][len(ELEC_YEARS) - 2 - i] for i in range(len(faction_distance[fc]))]
    # print(years)
    return faction_distance, years


def plot_pw_cl_distances():
    faction_distance, years = pairwise_cluster_distances()
    for c in faction_distance:
        plt.plot(years[c], faction_distance[c], label=f'{c[0]}-{c[1]}')
    plt.legend()
    plt.ylabel('Distance')
    plt.xlabel('Year')
    plt.show()


# Usage not recommended, plot looks shitty and is not very informative
def plot_all_legislatures():
    fig, axes = plt.subplots(5, 5)
    for i, year in enumerate(ELEC_YEARS[:-1]):
        G = createNXGraph(year, base_path=BUNDESTAG_GRAPH_PATH)
        ax = axes[i // 5, i % 5]
        nx.draw(G, nx.spring_layout(G, iterations=10), ax=ax, node_size=.01)
    # fig.tight_layout()
    plt.show()


def year_to_period(year):
    year = int(year)
    return f'{year}-{ELEC_YEARS[ELEC_YEARS.index(year) + 1]}'


def get_weight_list(G):
    weight_list = []
    for i, j in G.edges():
        weight_list.append(G[i][j]['weight'])
    return weight_list


def factions_for_range(G: nx.Graph, wrange=(.8, .85)) -> list:
    """Returns a list of tuples of factions from the politicians of that faction that have an edge with a weight in
    the given range.
    E.g. if the edge between Politician A and Politician B has a weight in the range
    then a tuple with their factions (plus weight) will be added to the list.
    """
    weights = []
    for u, v, data in G.edges(data=True):
        if wrange[0] <= data['weight'] <= wrange[1]:
            weights.append((u, v, data))
    result = []
    for w in weights:
        fac_tuple = sorted((G.nodes[w[0]]['cluster'], G.nodes[w[1]]['cluster']))
        result.append((fac_tuple[0], fac_tuple[1], w[2]))
    return result  # [(G.nodes[w[0]]['cluster'], G.nodes[w[1]]['cluster'], w[2]) for w in weights]


def max_faction_in_range(G, wrange=(.8, .85), n=8):
    """Returns the n factions with the most edges in the given weight range."""
    factions = factions_for_range(G, wrange)
    faction_count = {}
    for faction in factions:
        if faction[0] not in faction_count:
            faction_count[faction[0]] = 0
        if faction[1] not in faction_count:
            faction_count[faction[1]] = 0
        faction_count[faction[0]] += 1
        faction_count[faction[1]] += 1
    return sorted(faction_count, key=faction_count.get, reverse=True)[:n]


def max_faction_pair_in_range(G, wrange=(.8, 1), n=8):
    """Returns the n faction pairs with the most edges in the given weight range."""
    factions = factions_for_range(G, wrange)
    faction_count = {}
    for faction in factions:
        if (faction[0], faction[1]) not in faction_count:
            faction_count[(faction[0], faction[1])] = 0
        faction_count[(faction[0], faction[1])] += 1
    return sorted(faction_count, key=faction_count.get, reverse=True)[:n]


def plot_weights_hist(G, amount_bins=25):
    weights = get_weight_list(G)
    counts, hist = np.histogram(weights, bins=amount_bins)
    plt.hist(hist[:-1], bins=amount_bins, weights=counts / np.sum(counts), edgecolor='black')
    plt.show()


# Needs the year as input
def read_graph(year: int):
    G = nx.read_pajek(BUNDESTAG_GRAPH_PATH + year_to_period(year) + "/network" + year_to_period(year) + ".net")
    G = nx.convert_node_labels_to_integers(G, label_attribute='label')
    return G


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


def cluster_distances(G, print_distances=False):
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
    if print_distances:
        for c in cluster:
            print(c, cluster[c][0] / cluster[c][1])
    return cluster

# G = createNXGraph(2013, './graphs/Bundestag/')
# cluster_distances(G)
# print(get_weight_list(G))
