# Current Goal: Learn more from node embeddings now that the model can make predictions

import argparse
from gensim.models import Word2Vec
from meta_learning import node2vec


# Adapted from the node2vec paper: Scalable Feature Learning for Networks
def parse_args():
    """
    Specify arguments for node2vec/word2vec learning.
    """
    parser = argparse.ArgumentParser(description="Run node2vec.")

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

    return model


if __name__ == "__main__":

    import meta_fetching as mf
    import meta_handling as mh

    G = mh.read_graph("/Users/mattbowring/PycharmProjects/ClashRoyale/empty.gpickle")
    G = mf.build_graph(G, rank=10)

    args = parse_args()

    graph = node2vec.Graph(G, args.directed, args.p, args.q)
    graph.preprocess_transition_probs()
    walks = graph.simulate_walks(args.num_walks, args.walk_length)
    model = learn_embeddings(walks)
    print(model.wv.most_similar(positive=['88']))

    import meta_visualization as mv

    # plot of some Xbow deck nodes
    mv.tsne_similar_nodes('XBow-Top100', model, ['72', '99', '45', '77', '88'], 0.8, 'xbow100.png')
