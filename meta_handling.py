
# === Tools for modeling the Clash Royale universe ===

import networkx as nx
import itertools

# for later use
class Card:

    def __init__(self, name):
        self.name = name
        # dictionary containing a weight for each link to another card
        self.links = {}

    def getMostUsedWith(self, count=1):
        return sorted(self.links, key=self.links.get, reverse=True)[:count]

    def getUsageWith(self, other):
        if other in self.links:
            return self.links[other]
        else:
            return None

    def getLeastUsedWith(self):
        return min(self.links, key=self.links.get)

    def getMaxWeight(self):
        return max(self.links.values())

    # number of links attached
    def getDegree(self):
        return len(self.links)

    # sum of weights over all attached links
    def getStrength(self):
        return round(sum(self.links.values()), 3)

# for later use
class Deck:

    # add some persistent variable here
    def __init__(self, player, trophies, result, opponent):
        self.player = player
        self.trophies = trophies
        self.result = result
        self.opponent = opponent

    def getPlayer(self):
        return self.player

    def getTrophies(self):
        return self.trophies

    def getBattleResult(self):
        return self.result

    def getOpponent(self):
        return self.opponent


# Each card is mapped to a node index into the graph model -> THESE NEED TO BE FIXED
cardToIdx = {'ThreeMusketeers': 0,
             'Golem': 1,
             'RoyalRecruits': 2,
             'PEKKA': 3,
             'LavaHound': 4,
             'MegaKnight': 5,
             'RoyalGiant': 6,
             'EliteBarbarians': 7,
             'GiantSkeleton': 8,
             'GoblinGiant': 9,
             'Sparky': 10,
             'Barbarians': 11,
             'MinionHorde': 12,
             'Rascals': 13,
             'Balloon': 14,
             'Witch': 15,
             'Prince': 16,
             'Bowler': 17,
             'Executioner': 18,
             'CannonCart': 19,
             'ElectroDragon': 20,
             'RamRider': 21,
             'Giant': 22,
             'Wizard': 23,
             'RoyalHogs': 24,
             'SkeletonDragons': 25,
             'BabyDragon': 26,
             'DarkPrince': 27,
             'Hunter': 28,
             'Lumberjack': 29,
             'InfernoDragon': 30,
             'ElectroWizard': 31,
             'NightWitch': 32,
             'MagicArcher': 33,
             'Valkyrie': 34,
             'Musketeer': 35,
             'MiniPEKKA': 36,
             'HogRider': 37,
             'BattleRam': 38,
             'Zappies': 39,
             'FlyingMachine': 40,
             'Healer': 41,
             'Knight': 42,
             'Archers': 43,
             'Minions': 44,
             'Bomber': 45,
             'GoblinGang': 46,
             'SkeletonBarrel': 47,
             'Firecracker': 48,
             'SkeletonArmy': 49,
             'Guards': 50,
             'IceWizard': 51,
             'Princess': 52,
             'Miner': 53,
             'Bandit': 54,
             'RoyalGhost': 55,
             'Fisherman': 56,
             'MegaMinion': 57,
             'DartGoblin': 58,
             'ElixirGolem': 59,
             'Goblins': 60,
             'SpearGoblins': 61,
             'FireSpirits': 62,
             'Bats': 63,
             'WallBreakers': 64,
             'IceGolem': 65,
             'Skeletons': 66,
             'IceSpirit': 67,
             'BarbarianHut': 68,
             'XBow': 69,
             'ElixirCollector': 70,
             'GoblinHut': 71,
             'InfernoTower': 72,
             'Mortar': 73,
             'Tesla': 74,
             'BombTower': 75,
             'Furnace': 76,
             'GoblinCage': 77,
             'Cannon': 78,
             'Tombstone': 79,
             'Lightning': 80,
             'Rocket': 81,
             'Graveyard': 82,
             'Freeze': 83,
             'Poison': 84,
             'Fireball': 85,
             'Arrows': 86,
             'RoyalDelivery': 87,
             'GoblinBarrel': 88,
             'Tornado': 89,
             'Clone': 90,
             'Earthquake': 91,
             'Zap': 92,
             'Snowball': 93,
             'Rage': 94,
             'BarbarianBarrel': 95,
             'TheLog': 96,
             'Mirror': 97,
             'HealSpirit': 98
             }

# all 28 possible 2-pair combos between 8 cards in a deck
combos8 = itertools.combinations(range(8), 2)

# all 4851 possible 2-pair edge combos between 99 cards
combos99 = itertools.combinations(range(99), 2)


def create_empty_graph():
    """
    :return: an empty graph network with pre-assigned node attributes that model the reality of the game.
    """
    # The graph G is undirected with pre-linked nodes. Each node represents a card and shares a link to all other nodes.

    # - The node attributes establish the nature of the game.
    # - The pre-assigned edge represents usages between cards.
    # - Additional edge attributes will be artificially developed

    # More pushed decks -> better data representation

    # How do we define node attributes to model abilities?, i.e. we cannot hardcode 'drop rage-spell on death'.
    # The attributes should attempt to naturally represent our environment. What are our hyper-parameters?

    # - Explicit: rarity, cost, count, targets, range, hitspeed, speed, health*, ~damage*
    # - Implicit: flying, placement (regular, any), building

    # *Health and damage depend on card level, but this can be dealt with later. Do we assume stats from max level?

    # Initialize usage edges between all nodes
    G = nx.complete_graph(99)
    nx.set_edge_attributes(G, 0, 'usages')

    # G = nx.MultiGraph()
    # combos = itertools.combinations(range(99), 2)
    # attr_dict = {'usages': 0}
    # MultiGraph.add_edges_from(combos, attr_dict)

    # G.add_node(0, {'name': 'ThreeMusketeers',
    #                     'rarity': 'Rare',
    #                     'cost': 9,
    #                     'count': 3,
    #                     'targets': 'Air&Ground',
    #                     'flying': False,
    #                     'range': 6.0,
    #                     'hitspeed': 1.1,
    #                     'speed': 'Medium'
    #                     }
    #                 )

    # === Set Node Attributes for Each Card ===

    # Dictionary indexing ensures attributes are assigned node-wise
    # These (will eventually) match those found in the cardToIdx dictionary


    n_attributes = {0: {'name': 'ThreeMusketeers',
                        'rarity': 'Rare',
                        'cost': 9,
                        'count': 3,
                        'targets': 'Air&Ground',
                        'flying': False,
                        'range': 6.0,
                        'hitspeed': 1.1,
                        'speed': 'Medium'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {1: {'name': 'Golem',
                        'rarity': 'Epic',
                        'cost': 8,
                        'count': 1,
                        'targets': 'Buildings',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 2.5,
                        'speed': 'Slow'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {2: {'name': 'RoyalRecruits',
                        'rarity': 'Common',
                        'cost': 7,
                        'count': 6,
                        'targets': 'Ground',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.3,
                        'speed': 'Medium'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {3: {'name': 'PEKKA',
                        'rarity': 'Epic',
                        'cost': 7,
                        'count': 1,
                        'targets': 'Ground',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.8,
                        'speed': 'Slow'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {4: {'name': 'LavaHound',
                        'rarity': 'Legendary',
                        'cost': 7,
                        'count': 1,
                        'targets': 'Buildings',
                        'flying': True,
                        'range': 3.5,
                        'hitspeed': 1.3,
                        'speed': 'Slow'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {5: {'name': 'MegaKnight',
                        'rarity': 'Legendary',
                        'cost': 7,
                        'count': 1,
                        'targets': 'Ground',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.7,
                        'speed': 'Medium'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {6: {'name': 'RoyalGiant',
                        'rarity': 'Common',
                        'cost': 6,
                        'count': 1,
                        'targets': 'Buildings',
                        'flying': False,
                        'range': 5.0,
                        'hitspeed': 1.7,
                        'speed': 'Slow'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {7: {'name': 'EliteBarbarians',
                        'rarity': 'Common',
                        'cost': 6,
                        'count': 2,
                        'targets': 'Ground',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.7,
                        'speed': 'VeryFast'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {8: {'name': 'GiantSkeleton',
                        'rarity': 'Epic',
                        'cost': 6,
                        'count': 1,
                        'targets': 'Ground',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.5,
                        'speed': 'Medium'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {9: {'name': 'GoblinGiant',
                        'rarity': 'Epic',
                        'cost': 6,
                        'count': 1,
                        'targets': 'Buildings',
                        'flying': False,
                        'range': 2.0,
                        'hitspeed': 1.7,
                        'speed': 'Medium'
                        }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {10: {'name': 'Sparky',
                         'rarity': 'Legendary',
                         'cost': 6,
                         'count': 1,
                         'targets': 'Ground',
                         'flying': False,
                         'range': 5.0,
                         'hitspeed': 4.0,
                         'speed': 'Slow'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {11: {'name': 'Barbarians',
                         'rarity': 'Common',
                         'cost': 5,
                         'count': 5,
                         'targets': 'Ground',
                         'flying': False,
                         'range': 2.0,
                         'hitspeed': 1.4,
                         'speed': 'Medium'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {12: {'name': 'MinionHorde',
                         'rarity': 'Common',
                         'cost': 5,
                         'count': 5,
                         'targets': 'Air&Ground',
                         'flying': True,
                         'range': 2.0,
                         'hitspeed': 1.0,
                         'speed': 'Fast'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {13: {'name': 'Rascals',
                         'rarity': 'Common',
                         'cost': 5,
                         'count': 1,
                         'targets': 'Air&Ground',   # ISSUES
                         'flying': False,
                         'range': 5.0,
                         'hitspeed': 1.5,
                         'speed': 'Medium'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {14: {'name': 'Balloon',
                         'rarity': 'Epic',
                         'cost': 5,
                         'count': 1,
                         'targets': 'Buildings',
                         'flying': True,
                         'range': 2.0,
                         'hitspeed': 3.0,
                         'speed': 'Medium'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)
    # :=============================================:
    n_attributes = {15: {'name': 'Witch',
                         'rarity': 'Epic',
                         'cost': 5,
                         'count': 1,
                         'targets': 'Air&Ground',
                         'flying': False,
                         'range': 5.0,
                         'hitspeed': 1.1,
                         'speed': 'Medium'
                         }
                    }
    nx.set_node_attributes(G, n_attributes)


    return G

