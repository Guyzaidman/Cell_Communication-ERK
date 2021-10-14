import numpy as np
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import plate_loading as pl
import networkx as nx
import heatmap


def plot_delaunay(points):
    """
    plot the Delaunay graph with the set of points provided
    :param points: numpy array of 2d points ex. -> np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
    :return: None
    """
    tri = Delaunay(points)
    plt.triplot(points[:, 0], points[:, 1], tri.simplices)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.show()


def plot_voronoi(points):
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor)
    plt.show()


def create_graph(well, edges_threshold):
    nodes = []
    d_cells = {}
    i = 0
    for c in well.cells:
        nodes.append((i, {'cell': c}))
        d_cells[i] = c
        i += 1

    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            cor = d_cells[i].calc_ktr_correlation(d_cells[j])[0]
            if cor > edges_threshold:  # or cor < -0.7:
                edges.append((i, j))

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


def make_heatmap(well, above, below):
    l = len(well.cells)
    edges = np.zeros((l, l))
    for i in range(l):
        for j in range(l):
            # for j in range(i + 1, l):
            cor = well.cells[i].calc_ktr_correlation(well.cells[j])[0]
            if not below < cor < above:  # or cor < -0.7:
                edges[i][j] = cor

    return edges


p = r'C:\Guy\ordered_plates'
plate1 = pl.load_pickle_obj(p, 'Plate 1.1')
# plate2 = pl.load_pickle_obj(p, 'Plate 1.2')
plate3 = pl.load_pickle_obj(p, 'Plate 1.3')
# plate4 = pl.load_pickle_obj(p, 'Plate 2.1')
plate5 = pl.load_pickle_obj(p, 'Plate 2.2')
plate6 = pl.load_pickle_obj(p, 'Plate 2.3')
# plate7 = pl.load_pickle_obj(p, 'Plate 3.1')
# plate8 = pl.load_pickle_obj(p, 'Plate 3.2')
# plate9 = pl.load_pickle_obj(p, 'Plate 3.3')

dmso_wells = [plate3[49],
              plate5[48], plate5[49], plate6[48], plate6[49], plate1[42]]
# dmso_wells = [plate1[48], plate1[42], plate9[49]]

for dmso_well in dmso_wells:

    data = make_heatmap(dmso_well, 0.7, -0.7)
    heatmap.plot_heatmap(data, dmso_well.well_name, 'cool')
    # dmso_well.plot_correlation_distribution(20)

    G = create_graph(dmso_well, 0.7)
    d_pos = {}
    for i in range(len(G.nodes)):
        d_pos[i] = G.nodes[i]['cell'].get_cell_position(0)
    ei = nx.algorithms.centrality.estrada_index(G)
    print(ei)

    # plt.title(dmso_well.well_name)
    # plt.figure(figsize=(10, 5))
    # ax = plt.gca()
    # ax.set_title(dmso_well.well_name)

    # nx.draw(G, d_pos, node_size=10, width=0.1)
    # nx.draw(G, node_size=10, width=0.1)

    # nx.draw(G, with_labels=True, node_color='lightgreen', ax=ax)
    # _ = ax.axis('off')
    # plt.show()
