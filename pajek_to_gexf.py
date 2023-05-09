import networkx as nx

name ='Bundestag2021-2025'

G = nx.Graph(name = name)
with open("./" + name + ".net", 'r') as file:
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

    nx.write_gexf(G, name + '.gexf')