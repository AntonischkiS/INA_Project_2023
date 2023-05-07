import networkx as nx
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt
import scipy as sp

with open('stripped') as f:
    data = list(map(str.strip, f.readlines()))
data = data[4:]

G = defaultdict(list)
G1 = nx.Graph()
for line in tqdm(data[:5]):
    name, seqstr = line.split()
    seq = set(map(int, seqstr.split(',')[1:-1]))
    print(seq)
    for i in seq:
        for k in seq:
            if not i == k:
                if not G1.has_edge(i,k):
                    G1.add_edge(i,k, weight = 1)
                else:
                    G1[i][k]['weight'] = G1[i][k]['weight'] + 1

#widths = list(nx.get_edge_attributes(G1,'weight').values())
print(G1[2][1]['weight'])
pos=nx.spring_layout(G1)
for u,v in G1.edges:
    if G1[u][v]['weight'] == 1:
        G1.remove_edge(u,v)



for i in G1.nodes:
    if G1.degree(i) == 0:
        G1.remove_node(i)


nx.draw_networkx(G1,pos)

'''
    for n in seq:
        G[n].append(name)

print(len(G))
'''

'''
pos=nx.spring_layout(G1) # pos = nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx(G1,pos)
labels = nx.get_edge_attributes(G1,'weight')
nx.draw_networkx_edge_labels(G1,pos,edge_labels=labels)
'''
plt.show()