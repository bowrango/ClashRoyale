
#  ClashRoyale

Decks used by the top players in the world are recorded using the offical Clash Royale API. Each card is assigned to a characterizing node that track its usage to other cards. By recieving these decks, a graph network is created, which attempts to model how the cards are used together based on their specific attributes. The node2vec algorithm is implemented to obtain a feature vector for each node (card) in the graph, which loosely descibes how the cards interact with one another. Since the graph network is non-Euclidean by nature, node2vec's feature vectors represent the usage data in a Euclidean space, which can then be passed to a traditional machine learning pipeline. With this, we can not only understand which cards are commonly used in a deck, but more importantly why certain card attributes make a strong deck. This project is currently under development, and is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

This acts as a wrapper around the networkx library which provides a flexible data strucure for graphs. The current goal is to develop a GNN to make predictions about which card is the best play in a specific scenario. Eventually, the model could be deployed to a bot that continously plays Clash Royale and learns from its mistakes.

# Usage

An empty graph can be initialized, which contains all pre-assigned node attributes
```
import meta_handling as mh
G = mh.read_graph(empty.gpickle)
```
The graph can then be updated with deck information. The `rank` parameter determines how many decks should be obtained from the top players. A graph with `rank=1` simply takes the current deck of the top player, while `rank=500` takes 500 decks from the respective top 500 players. This method accesses the offical API, and updates the respective edge weights for each deck.
```
import meta_fetching as mf
G = mf.build_graph(G, rank=500)
```


"This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy."
