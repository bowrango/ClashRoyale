#  ClashRoyale

Usage rates of various cards/decks in Clash Royale are scraped from StatsRoyale.com. Each card is assigned a characterizing node that tracks its usage to other cards. These relations are detemined from each deck used by the top 200 players on ladder. All this data is then processed to highlight changes in the meta as players shift their play style. This project is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

This acts as a wrapper around the networkx library which provides a flexible data strucure for graphs. The current goal is to develop a GNN to make predictions about which card is the best play in a specific scenario. Eventually, the model could be deployed to a bot that continous plays Clash Royale and learns from its mistakes.

# Methods
Lists are scraped from the web, each containing a string for each card used in a deck. Each card is trated as a node in a graph network, all nodes share an adjacent edge which stores the number of times the two cards have been used together in a deck. By providing the model with more deck information, a better representation is obtained. Creating an empty graph will initialize all node attributes, which are obtained dynamically, i.e. the data is scarped from StatsRoyale.com. 

```
import meta_fetching as mf
G = mh.create_empty_graph()
```
The user can then determine how many how decks are used to build up the graph model:
```
G = mf.build_graph(G, decks=500)
```
The adjacency matrix for the `usages` edge attribute can shown:
'''
import meta_visualization as mv
show_usage_matrix(G)
```


