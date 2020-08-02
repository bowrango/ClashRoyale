#  ClashRoyale

Usage rates of various cards/decks in Clash Royale are scraped from StatsRoyale.com. Each card is assigned a node that links its usage to other cards. These relations are detemined within each deck from the top 200 players on ladder. All this data is then processed to highlight changes in the meta as players shift their play style. The goal is to determine which cards are commonly used together, and how their attributes translate to winning gameplay. This project is really just an outlet to explore and gain experience in the graph ML space, while investigating a superb game. 

## Use

The primary output is a `numpy.array` containing the weighted adjacency matrix of all 99 cards in the game. When cards are used together in a deck, their weights are linked respectively to the other cards in the deck. For example, Icebow is a infamously popular deck, which relies on the strong Xbow /  Ice Wizard combo. A typical deck might look like:

`['XBow', 'IceWizard', 'Skeletons', 'Rocket', 'IceGolem', 'MegaMinon', 'TheLog', 'Tornado']`


