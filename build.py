
import meta_handling as mh

# save an empty graph with assigned node attributes
if __name__ == '__main__':

    import meta_handling as mh
    G = mh.create_empty_graph()
    
    graph = mh.save_graph(G, "empty.gpickle")

    # import meta_handling as mh
    # import meta_fetching as mf
    # G = mh.read_graph('empty.gpickle')
