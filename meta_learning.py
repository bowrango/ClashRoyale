# Current Goal: Make a prediction for the best card to play given another card, i.e. which card is the best counter?

import networkx as nx
import meta_handling as mh
import meta_fetching as mf

import numpy as np

temp = mh.create_empty_graph()

G = mf.build_graph(temp, decks=100)

L = nx.linalg.laplacianmatrix.laplacian_matrix(G, weight='usages')
D = nx.degree(G)
D_inv = np.linalg.inv(D)