from utils import info, plot_weights_hist, createNXGraph, cluster_distances

for i in range(2013, 2022, 4):
    G = createNXGraph(i)
    # info(G)
    plot_weights_hist(G)
    # print("================================")
    # print("For year", i, ":")
    # cluster_distances(G)



