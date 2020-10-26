# === Tools for visualizing the Clash Royale universe ===

import numpy as np
from chord import Chord

def get_usage_matrix(G):
    """
    :param G: networkx graph object
    :return: adjacency matrix of weighted usages
    """
    return None

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

def create_chord_diagram(matrix, labels):
    """
    :param matrix: adjacency matrix of weighted usages
    :param labels: names of all cards
    :return: chord html file
    """
    Chord(matrix, labels).to_html()