
#  ClashRoyale

Decks used by the top players in the world are recorded using a custom wrapper for the official Clash Royale API. Each card is assigned to a characterizing node that track its usage to other cards. By recieving these decks, a graph network is created, which attempts to model how the cards are used together based on their specific attributes. The node2vec algorithm is implemented to obtain a feature vector for each node (card) in the graph, which loosely descibes how the cards interact with one another. Since the graph network is non-Euclidean by nature, node2vec's feature vectors represent the usage data in a Euclidean space, which can then be passed to a traditional machine learning pipeline. With this, we can not only understand which cards are commonly used in a deck, but more importantly why certain card attributes make a strong deck. This project is currently under development, and is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 


# Usage

This repo will provide many functionalities in time for analyzing player trends with Bayesian graph networks; perhaps even ones with factors. Here is some demo code to show off the API:

```
from RoyaleAPI import Client
proxy_url = 'https://proxy.royaleapi.dev/v1'

client = Client(token=dev_key, url=proxy_url)
top_decks = client.get_top_decks(limit=3)

print(top_decks)
```

```
[
['Royal Giant', 'Royal Ghost', 'Fisherman', 'Electro Spirit', 'Skeletons', 'Fireball', 'The Log', 'Tesla'],
 ['Lava Hound', 'Balloon', 'Earthquake', 'Arrows', 'Minions', 'Bomber', 'Inferno Dragon', 'Miner'], 
 ['Lava Hound', 'Balloon', 'Skeletons', 'Arrows', 'Minions', 'Bomber', 'Inferno Dragon', 'Miner']
 ]
```

Note that you must pass in your own `dev_key`, which can be obtained by [creating a Clash Royale API account](https://developer.clashroyale.com/#/register).

# Disclaimer

This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.
