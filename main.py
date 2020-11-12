import networkx as nx

import meta_handling as mh
import meta_fetching as mf
import meta_visualization as mv
from meta_handling import cardToIdx

import numpy as np
from chord import Chord

if __name__ == '__main__':

    # template = mh.create_empty_graph()
    # G = mf.build_graph(template, decks=5000)
    # mv.show_usage_matrix(G)
    #
    G = nx.complete_graph(101)
    nx.set_edge_attributes(G, 0, 'usages')

    # create some fake data
    import itertools
    combos = itertools.combinations(range(101), 2)
    for u, v in combos:
        G[u][v]['usages'] = np.random.randint(0, 5)

    mv.show_chord_diagram(G)



