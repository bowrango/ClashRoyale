
import networkx as nx
import meta_fetching as mf
import meta_visualization as mv

import time

# Fetch data from ladder
if __name__ == '__main__':

    t0 = time.perf_counter()

    # Specify how many decks a graph should be representative of
    G1 = mf.build_graph(decks=1)
    # G2 = mf.build_graph(decks=10)
    # G3 = mf.build_graph(decks=100)
    # G4 = mf.build_graph(decks=1000)

    t1 = time.perf_counter()
    print(f"Build Time: {round(t1-t0, 5)}")








