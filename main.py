
import meta_handling as mh

if __name__ == '__main__':

    # save an empty graph with assigned node attributes
    # import meta_handling as mh
    # G = mh.create_empty_graph()
    #
    # graph = mh.save_graph(G, "empty.gpickle")

    import meta_handling as mh
    import meta_fetching as mf
    G = mh.read_graph('empty.gpickle')

    G = mf.build_graph(G, rank=5)
    print('hello')