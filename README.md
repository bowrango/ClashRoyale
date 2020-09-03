#  ClashRoyale

Usage rates of various cards/decks in Clash Royale are scraped from StatsRoyale.com. Each card is assigned a characterizing node that tracks its usage to other cards. These relations are detemined from each deck used by the top 200 players on ladder. All this data is then processed to highlight changes in the meta as players shift their play style. The goal is to determine which cards are commonly used together, and how their attributes translate to winning gameplay. This project is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

# Methods
Lists are scraped from the web, each containaining a string for each card. These lists, representing a deck, are fed into a graph model to update parameters. The user can specify how many decks a model should be representative of:

```
import meta_handling as mf
G = mf.build_graph(decks=500)
```

This acts as a wrapper around on the networkx graph library. The [base graph object](https://networkx.github.io/documentation/stable/reference/generated/networkx.generators.classic.complete_graph.html?highlight=complete_graph#networkx.generators.classic.complete_graph) contains pre-assigned edges between all nodes. These edges track the 
