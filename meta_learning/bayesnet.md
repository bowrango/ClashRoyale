
Game Semantics with Bayesian Networks
-----

The fundamental characteristic of a top player in Clash Royale is shown through the mastery of game mechanics utilized in constructing decks and predicting opponent behavior. 

General Goal: Given the cards I have observed from the opponent, what is the most likely action sequence I can take to maximize my chance of success?

The idea is to create a Bayesian Network where all nodes share a directed 
influence on each other since we cannot hardcode a topological ordering of dependence. This complete network requires `n2^{n-1}` probabilities to represent the full domain -- so for `n = 102` it is clear the network needs to be more compact. Luckily, the deck usages are locally structured, i.e. we see sparse representations in the usage adjacency matrix. This means we can focus on the most important conditional probabilities: those that capture the inherent structure in the most commonly used decks. This allows for a powerful tradeoff between model complexity and accuracy.  

This all assumes we know nothing of the opponent's hand aside from being a set of 8 unique nodes. As cards are played, however, the objective of the model is to devise which other cards are most likely to be contained within the set. A priori knowledge about the node attributes could possibly be leveraged in decision making as this is the strength of high-skilled players. 

- The model has at most 4 (from a total set of 8) discrete actions it can take in a continous game space. 

- The set of 4 possible actions (the current cards in hand) change as they are played. The starting hand is random.

- The actions are limited due to an elixir cost assiociated with playing each card. This is a significant attribute, as the elixir capacity is small relative to the cost of playing a card. Both players have the same elixir capacity.

- Cards can be played within an (x, y) grid. Placement is also a key component.


