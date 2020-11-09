# === Tools for visualizing the Clash Royale universe ===

import networkx as nx
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from chord import Chord

from meta_handling import cardToIdx


# normalizes data in the 2D numpy array, controls how we see the chord diagram
def normalize_weights(array):
    """
    :param array: the 2D 'adjacency matrix' which contains the weights
    :return: the normalized matrix, along its maximums
    """
    # gets max of flattened array
    normalizer = np.amax(array)

    # x -> x/max(x) for all x in array with 0 <= x <= 1
    for idx, weightedArray in enumerate(array):
        array[idx] = np.true_divide(weightedArray, normalizer)

    return array, normalizer

def show_usage_matrix(G):
    """
    :param G: networkx graph object
    :return: None
    """

    matrix = nx.convert_matrix.to_numpy_array(G, weight='usages')

    image = plt.imshow(matrix)
    plt.title(f"Decks Used: {G.graph['decks']}")


def show_chord_diagram(G):
    """
    :param G: networkx graph object
    :return: chord html file
    """

    # TODO: Check out code from Stami to fix this. There is an error in the returned HTML file.
    adj_matrix = nx.convert_matrix.to_numpy_array(G)
    # Prob can get this form the graph directly
    labels = cardToIdx.keys()

    Chord(adj_matrix, labels).to_html()