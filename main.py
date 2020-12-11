
import meta_handling as mh

if __name__ == '__main__':

    G = mh.create_empty_graph()
    from meta_handling import save_graph

    graph = save_graph(G, "empty.gpickle")