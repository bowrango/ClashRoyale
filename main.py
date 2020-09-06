
import networkx as nx
import meta_fetching as mf
import meta_handling as mh
import meta_visualization as mv

# Fetch data from ladder
if __name__ == '__main__':


    # # Specify how many decks a graph should be representative of
    G1 = mf.build_graph(decks=10)

    print(nx.density(G1))






