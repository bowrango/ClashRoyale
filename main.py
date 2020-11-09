
import networkx as nx
import numpy

import meta_handling as mh
from meta_handling import cardToIdx

import meta_fetching as mf
import meta_visualization as mv


# Fetch data from ladder
if __name__ == '__main__':


    # # Specify how many decks a graph should be representative of
    G = mf.build_graph(decks=10)

    mv.show_usage_matrix(G)

    print(nx.density(G))








