# === Tools for visualizing the Clash Royale universe ===

import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from chord import Chord

from meta_handling import idxToCard

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


def visualize_edge_matrix(G, weight=None, type='heatmap'):
    """
    :param weight: the edge attribute
    :param type: type of plot to be shown
    :param G: networkx graph object
    :return: None
    """
    if type is 'heatmap':
        matrix = nx.convert_matrix.to_numpy_array(G, weight=weight)
        plt.imshow(matrix, cmap='hot')
        plt.show()

    if type is 'degree':
        degs = nx.degree(G, weight=weight)
        degree = [i[1] for i in degs]

        # scaled down
        sorted_deg = sorted(np.divide(degree, 7))
        sorted_labels = [G.nodes[i]['name'] for i in np.argsort(degree)]

        plt.plot(range(len(sorted_deg)), sorted_deg)
        plt.xticks(ticks=range(len(sorted_labels)),
                   labels=sorted_labels,
                   rotation='vertical',
                   fontsize=5)
        plt.margins(0.05)
        plt.show()


def show_chord_diagram(G):
    """
    :param G: networkx graph object
    :return: chord html file
    """
    # TODO: Create a copy of the graph with the 0 edge weights removed, i.e. only show cards that have
    #  been used together. We can consider a new graph with only the significant edges.
    matrix = nx.convert_matrix.to_numpy_array(G, weight='usages')
    matrix = matrix.tolist()
    #
    # labels = list(cardToIdx.keys())
    # Chord(matrix, labels).to_html()


def tsne_similar_nodes(title, mdl, nodes, a, filename=None):

    from sklearn.manifold import TSNE

    embedding_clusters = []
    word_clusters = []

    for word in nodes:

        embeddings = []
        words = []

        for similar_word, _ in mdl.wv.most_similar(word, topn=30):
            words.append(similar_word)
            embeddings.append(mdl.wv[similar_word])

        embedding_clusters.append(embeddings)
        word_clusters.append(words)

    embedding_clusters = np.array(embedding_clusters)
    n, m, k = embedding_clusters.shape
    tsne_model_in_2d = TSNE(perplexity=15, n_components=2, init='pca', n_iter=3500, random_state=32)
    embeddings_in_2d = np.array(tsne_model_in_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)

    plt.figure(figsize=(16, 9))

    for label, embeddings, words in zip(nodes, embedding_clusters, word_clusters):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        card_name = idxToCard[int(label)]
        plt.scatter(x, y, alpha=a, label=card_name)

        for i, word in enumerate(words):
            # word -> card_name thru map
            card = idxToCard[int(word)]
            plt.annotate(card, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
                         textcoords='offset points', ha='right', va='bottom', size=8)
    plt.legend(loc=4)
    plt.title(title)
    plt.grid(True)

    if filename:
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
    plt.show()