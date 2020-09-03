
# === Tools for modeling the Clash Royale universe ===

import networkx as nx

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
cardToIdx = {'Archers': 0,
             'BabyDragon': 1,
             'Balloon': 2,
             'Bandit': 3,
             'Barbarians': 4,
             'Bats': 5,
             'BattleHealer': 6,
             'BattleRam': 7,
             'Bomber': 8,
             'Bowler': 9,
             'CannonCart': 10,
             'DarkPrince': 11,
             'DartGoblin': 12,
             'ElectroDragon': 13,
             'ElectroWizard': 14,
             'EliteBarbarians': 15,
             'ElixirGolem': 16,
             'Executioner': 17,
             'Firecracker': 18,
             'FireSpirits': 19,
             'Fisherman': 20,
             'FlyingMachine': 21,
             'Giant': 22,
             'GiantSkeleton': 23,
             'GoblinCage': 24,
             'GoblinGang': 25,
             'GoblinGiant': 26,
             'Goblins': 27,
             'Golem': 28,
             'Guards': 29,
             'HogRider': 30,
             'Hunter': 31,
             'HealSpirit': 32,
             'IceGolem': 33,
             'IceSpirit': 34,
             'IceWizard': 35,
             'InfernoDragon': 36,
             'Knight': 37,
             'LavaHound': 38,
             'Clone': 39,
             'Lumberjack': 40,
             'MagicArcher': 41,
             'MegaMinion': 42,
             'MegaKnight': 43,
             'MiniPEKKA': 44,
             'Miner': 45,
             'Minions': 46,
             'MinionHorde': 47,
             'Musketeer': 48,
             'NightWitch': 49,
             'PEKKA': 50,
             'Prince': 51,
             'Princess': 52,
             'RamRider': 53,
             'RoyalGhost': 54,
             'RoyalGiant': 55,
             'RoyalHogs': 56,
             'RoyalRecruits': 57,
             'Skeletons': 58,
             'SkeletonArmy': 59,
             'SkeletonBarrel': 60,
             'SkeletonDragons': 61,
             'Sparky': 62,
             'SpearGoblins': 63,
             'ThreeMusketeers': 64,
             'Valkyrie': 65,
             'WallBreakers': 66,
             'Witch': 67,
             'Wizard': 68,
             'Zappies': 69,
             'BombTower': 70,
             'Cannon': 71,
             'InfernoTower': 72,
             'Mortar': 73,
             'Tesla': 74,
             'XBow': 75,
             'BarbarianHut': 76,
             'ElixirCollector': 77,
             'Furnace': 78,
             'GoblinHut': 79,
             'Tombstone': 80,
             'Arrows': 81,
             'BarbarianBarrel': 82,
             'Earthquake': 83,
             'Fireball': 84,
             'Freeze': 85,
             'GiantSnowball': 86,
             'Lightning': 87,
             'Poison': 88,
             'Rocket': 89,
             'RoyalDelivery': 90,
             'TheLog': 91,
             'Tornado': 92,
             'Zap': 93,
             'Rascals': 94,
             'Mirror': 95,
             'Graveyard': 96,
             'Rage': 97,
             'GoblinBarrel': 98
             }


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

