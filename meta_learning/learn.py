# Current Goal: Create node embeddings.

import argparse
import networkx as nx
import numpy as np
from gensim.models import Word2Vec
from meta_learning import node2vec


# Adapted from the node2vec implementation by Aditya Grover
def parse_args():
    """
    Specify arguments for node2vec/word2vec learning.
    """
    parser = argparse.ArgumentParser(description="Run node2vec.")

    # This argument could be removed
    # parser.add_argument('--input', nargs='?', default='output/karate.edgelist',
    #                     help='Input graph path')

    parser.add_argument('--output', nargs='?', default='output/cards.emb',
                        help='Embeddings path')

    # Check to make sure this dim is correct...I believe it is
    parser.add_argument('--dimensions', type=int, default=101,
                        help='Number of dimensions. Default is 128.')

    parser.add_argument('--walk-length', type=int, default=80,
                        help='Length of walk per source. Default is 80.')

    parser.add_argument('--num-walks', type=int, default=10,
                        help='Number of walks per source. Default is 10.')

    parser.add_argument('--window-size', type=int, default=10,
                        help='Context size for optimization. Default is 10.')

    parser.add_argument('--iter', default=1, type=int,
                        help='Number of epochs in SGD')

    parser.add_argument('--workers', type=int, default=8,
                        help='Number of parallel workers. Default is 8.')

    parser.add_argument('--p', type=float, default=1,
                        help='Return hyperparameter. Default is 1.')

    parser.add_argument('--q', type=float, default=1,
                        help='Inout hyperparameter. Default is 1.')

    parser.add_argument('--weighted', dest='weighted', action='store_true',
                        help='Boolean specifying (un)weighted. Default is unweighted.')
    parser.add_argument('--unweighted', dest='unweighted', action='store_false')
    parser.set_defaults(weighted=True)

    parser.add_argument('--directed', dest='directed', action='store_true',
                        help='Graph is (un)directed. Default is undirected.')
    parser.add_argument('--undirected', dest='undirected', action='store_false')
    parser.set_defaults(directed=False)

    return parser.parse_args()


# def read_graph():
#     """
#     Reads the input network in networkx.
#     """
#
#     # This seems to rebuild the graph from the raw edge data. We already have a graph to use
#     if args.weighted:
#         G = nx.read_edgelist(args.input, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
#     else:
#         G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
#         for edge in G.edges():
#             G[edge[0]][edge[1]]['weight'] = 1
#
#     if not args.directed:
#         G = G.to_undirected()
#
#     return G


def learn_embeddings(walks):
    """
    Learn embeddings by optimizing the Skipgram objective using SGD.
    """
    # all nodes indices are turned into words from integers
    walks = [[str(s) for s in walk] for walk in walks]

    model = Word2Vec(walks, size=args.dimensions,
                     window=args.window_size,
                     min_count=0,
                     sg=1,
                     workers=args.workers,
                     iter=args.iter)

    # Figure this out later
    # model.wv.save_word2vec_format(args.output)

    return


# def learn(args):
#     """
#     Pipeline for representational learning for all nodes in a graph.
#     """
#     # This could be replaced by one of my own graphs
#     nx_G = read_graph()
#     G = node2vec.Graph(nx_G, args.directed, args.p, args.q)
#     G.preprocess_transition_probs()
#     walks = G.simulate_walks(args.num_walks, args.walk_length)
#     learn_embeddings(walks)


if __name__ == "__main__":
    args = parse_args()
    # learn(args)

    nx_G = nx.complete_graph(101)
    import itertools

    combos = itertools.combinations(range(101), 2)
    for u, v in combos:
        nx_G[u][v]['usages'] = np.random.randint(0, 5)

    G = node2vec.Graph(nx_G, args.directed, args.p, args.q)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(args.num_walks, args.walk_length)
    learn_embeddings(walks)
    print(walks)
