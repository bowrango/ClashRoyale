# Current Goal: Make a prediction for the best card to play given another card, i.e. which card is the best counter?

import networkx as nx
import meta_handling as mh
import meta_fetching as mf

import numpy as np

e = mh.create_empty_graph()
G = mf.build_graph(e, decks=100)

L_norm = nx.linalg.laplacianmatrix.normalized_laplacian_matrix(G, weight='usages')
D = nx.degree(G)
