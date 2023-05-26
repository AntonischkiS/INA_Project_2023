from tabulate import tabulate
from utils import *  # info, plot_weights_hist, createNXGraph, cluster_distances, factions_for_range

# plot_all_legislatures()
# plot_pw_cl_distances()
dists = in_cluster_distance(2017)
print(tabulate(dists, headers=['Faction', 'Distance', 'Absence excluded distance'], tablefmt="latex", floatfmt=".4f"))
# for i in range(2013, 2014, 4):
#     G = createNXGraph(i)
#     # info(G)
#     plot_weights_hist(G)
#     # print("================================")
#     # print("For year", i, ":")
#     # cluster_distances(G)
#     # print(factions_for_range(G))
#     # print(max_faction_in_range(G, (.2, .4)))
#     # print(max_faction_pair_in_range(G, (.2, .4)))
#     # print(max_faction_in_range(G, (0, .2)))
#     print(max_faction_pair_in_range(G, (0, .2)))
