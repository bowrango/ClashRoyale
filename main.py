
from RoyaleAPI import Client
import networkx as nx
import matplotlib.pyplot as plt 

with open('RoyaleAPI/key.txt', 'r') as file:
        dev_key = file.read().replace('\n', '')
proxy_url = 'https://proxy.royaleapi.dev/v1'

# client = Client(token=dev_key, url=proxy_url)
# graph = client.create_empty_graph()

# top_graph = client.build_graph(graph, topn=1)

# nx.draw(top_graph)
# nx.draw_networkx_edges(top_graph, pos=nx.spring_layout(top_graph))
# nx.draw_circular(top_graph, with_labels=True)
# nx.draw_spectral(top_graph, with_labels=True)
# plt.show()

# analysis
# cltr = nx.within_inter_cluster(top_graph)
# density = nx.density(top_graph)
# histogram = nx.degree_histogram(top_graph)
# cliques = list(nx.find_cliques(top_graph))

client = Client(token=dev_key, url=proxy_url)
graph = client.create_empty_graph()
top_graph = client.build_graph(graph, topn=10)

# elixir_costs = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
# probs = nx.attr_matrix(top_graph, node_attr="elixir", normalized=True, rc_order=elixir_costs)
# print(probs)

types = [str(i+1) for i in range(10)]

# TODO: handle RuntimeWarning when normalizing by an empty row -> inserts nan 
probs = nx.attr_matrix(top_graph, node_attr="elixir", edge_attr='usages', normalized=True, rc_order=types)
print(probs)
