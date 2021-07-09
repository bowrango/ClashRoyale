
#  ClashRoyale

Decks used by the top players in the world are recorded using a custom wrapper for the official Clash Royale API. Each card is assigned to a characterizing node that track its usage to other cards. By recieving these decks, a graph network is created, which attempts to model how the cards are used together based on their specific attributes. The node2vec algorithm is implemented to obtain a feature vector for each node (card) in the graph, which loosely descibes how the cards interact with one another. Since the graph network is non-Euclidean by nature, node2vec's feature vectors represent the usage data in a Euclidean space, which can then be passed to a traditional machine learning pipeline. With this, we can not only understand which cards are commonly used in a deck, but more importantly why certain card attributes make a strong deck. This project is currently under development, and is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

Using this data, I'd like to develop a more refined Bayesian Network that makes decisions to minic player behavior. 

# Usage

The `RoyaleAPI` acts as an intermediary in converting JSON responses into `networkx` graph structures. A JSON Web Token is used for request authorization, so you must pass in your own `dev_key`, which can be obtained by [creating a Clash Royale API account](https://developer.clashroyale.com/#/register). [A proxy solution is also used](https://docs.royaleapi.com/#/).

This project aims to provide many functionalities in time for analyzing player trends with graph structures. Here is some demo code to show off the API:
```
from RoyaleAPI import Client

# save your own developer key to a key.txt file into the RoyaleAPI directory
with open('RoyaleAPI/key.txt', 'r') as file:
    dev_key = file.read().replace('\n', '')
proxy_url = 'https://proxy.royaleapi.dev/v1'

# build a graph representing cards used by the top 100 players in the world
client = Client(token=dev_key, url=proxy_url)
graph = client.create_empty_graph()
top100_graph = client.build_graph(graph, depth=100)
```

All the regular `networkx` methods can then be utilized for analysis:
```
import networkx as nx
print(nx.density(top100_graph))
```

# Disclaimer

This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.
