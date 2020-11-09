#  ClashRoyale

Usage rates of various cards/decks in Clash Royale are scraped from StatsRoyale.com. Each card is assigned a characterizing node that tracks its usage to other cards. These relations are detemined from each deck used by the top 200 players on ladder. All this data is then processed to highlight changes in the meta as players shift their play style. The goal is to determine which cards are commonly used together, and how their attributes translate to winning gameplay. This project is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

# Methods
Lists are scraped from the web, each containing a string for each card used in a deck. These decks are fed into a graph model which stores node attributes for each card. By providing the model with more deck information, a better representation is obtained. The user can specify how many decks a model should be representative of:

```
import meta_handling as mf
G = mf.build_graph(decks=500)
```

This acts as a wrapper around the networkx graph library. The [base graph object](https://networkx.github.io/documentation/stable/reference/generated/networkx.generators.classic.complete_graph.html?highlight=complete_graph#networkx.generators.classic.complete_graph) contains pre-assigned edges between all nodes. For the 99 different cards in the game, there exists 4851 edges in the model, i.e.  `combinations(99,2)`. Since cards are used together in a deck, the unique combination pairs are represented. The weights of these 4851 edges are initialized, and are updated each time a deck is pushed to the parent graph network.

The current goal is to develop a GNN to make predictions about which card would be the best play in a particular circumstance. This model could then be deployed to play Clash Royale and learn while doing so.  
