
#  ClashRoyale

Decks used by the top players in the world are recorded using a custom wrapper for the official Clash Royale API. Each card is assigned to a characterizing node that track its usage to other cards. By recieving these decks, a graph network is created, which attempts to model how the cards are used together based on their specific attributes. The node2vec algorithm is implemented to obtain a feature vector for each node (card) in the graph, which loosely descibes how the cards interact with one another. Since the graph network is non-Euclidean by nature, node2vec's feature vectors represent the usage data in a Euclidean space, which can then be passed to a traditional machine learning pipeline. With this, we can not only understand which cards are commonly used in a deck, but more importantly why certain card attributes make a strong deck. This project is currently under development, and is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 


# Usage

This repo will provide many functionalities for analyzing player trends with (hopefully) Bayesian graph networks, perhaps with factors. Here is some demo code to view the decks used by the top players in the world. These are simple API calls utilizing a proxy that recieve data.

```
from RoyaleAPI import Client

client = Client(token=your_dev_key)
players = c.get_top_players(limit=10)

for player in players.raw_data:
    tag = player.raw_data['tag']
    player_info = c.get_player(tag)
    current_deck = player_info.raw_data['currentDeck']
    current_deck = [dict_idx['name'] for dict_idx in current_deck]
    print(current_deck)
```


# Disclaimer

This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.
