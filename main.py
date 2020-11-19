import networkx as nx

import meta_handling as mh
import meta_fetching as mf
import meta_visualization as mv
from meta_handling import cardToIdx

import numpy as np
from chord import Chord
import pickle

import matplotlib.pyplot as plt

if __name__ == '__main__':

    e = mh.create_empty_graph()
    G = mf.build_graph(e, decks=1)
    mv.show_edge_matrix(G, weight='usages', type='degree')

    # fabricate some test data
    # import itertools
    # combos = itertools.combinations(range(101), 2)
    # for u, v in combos:
    #     G[u][v]['usages'] = np.random.randint(0, 5)

    # super uber mega data gulp
    # N = 25

    # T = np.zeros(shape=(N, 101, 101))
    # for k in range(0, N):
    #
    #     data = mf.build_graph(G, decks=k*100)
    #     datamat = nx.convert_matrix.to_numpy_array(data, weight='usages')
    #
    #     T[k] = datamat
    #
    # np.save('bigdata', T)
