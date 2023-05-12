import networkx as nx
import utils
import sys
from pathlib import Path

#name ='Bundestag2021-2025'

def pajek_to_gexf(base_path, leg_year):
    G = nx.Graph()
    leg_period = utils.year_to_period(leg_year)
    filename_stem = "network"+leg_period
    with open(base_path+leg_period+'/'+filename_stem+'.net', 'r') as file:
        file.readline()

        for line in file:
            if line.startswith("*"):
                break
            else:
                node = line.strip(' ')
                node = node.split("\"")
                G.add_node(int(node[0]) - 1, label = node[1])
                if node[7] == 'yellow':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 255, 'g': 255, 'b': 0, 'a': 0}}
                elif node[7] == 'black':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}}
                elif node[7] == 'red':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 255, 'g': 0, 'b': 0, 'a': 0}}
                elif node[7] == 'blue':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 0, 'g': 0, 'b': 255, 'a': 0}}
                elif node[7] == 'green':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 0, 'g': 255, 'b': 0, 'a': 0}}
                elif node[7] == 'magenta':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 255, 'g': 0, 'b': 255, 'a': 0}}
                elif node[7] == 'grey':
                    G.nodes[int(node[0]) - 1]['viz'] = {'color': {'r': 128, 'g': 128, 'b': 128, 'a': 0}}

        for line in file:
            i, j, v = line.split()
            G.add_edge(int(i) - 1, int(j) - 1, weight = v)

        nx.write_gexf(G, base_path + leg_period + '/' + filename_stem + '.gexf')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("must specify election year")
        exit()
    if sys.argv[1] not in utils.YEAR_TO_LEG_ID:
        print("invalid election year")
        exit()
    leg_year = sys.argv[1]
    pajek_to_gexf(utils.BUNDESTAG_GRAPH_PATH, leg_year)