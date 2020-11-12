# === Tools for visualizing the Clash Royale universe ===

import networkx as nx
import numpy as np

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

    # 2D heatmap
    matrix = nx.convert_matrix.to_numpy_array(G, weight='usages')
    plt.imshow(matrix, cmap='hot')
    plt.show()

    # nx.draw(G, with_labels=True)
    # plt.draw()
    # plt.show()


def show_chord_diagram(G):
    """
    :param G: networkx graph object
    :return: chord html file
    """

    # Create a copy of the graph with the 0 edge weights removed, i.e. only show cards that have
    # been used together. We can consider a new graph with only the significant edges.
    matrix = nx.convert_matrix.to_numpy_array(G, weight='usages')
    matrix = matrix.tolist()

    labels = list(cardToIdx.keys())

    Chord(matrix, labels).to_html()
