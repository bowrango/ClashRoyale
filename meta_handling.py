
# === Classes/Methods for modelling the Clash Royale universe ===

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


def create_empty_graph():
    """
    :return: Creates an empty graph network where the node attributes control the reality of the game.
    """
    import networkx as nx
    G = nx.Graph()

    G.add_node('ThreeMusketeers',
               rarity='Rare',
               cost=9,
               count=3,
               targets='Air&Ground',
               flying=False,
               range=6.0,
               hitspeed=1.1,
               speed='Medium'
               )

    G.add_node('Golem',
               rarity='Epic',
               cost=8,
               count=1,
               targets='Buildings',
               flying=False,
               range=2.0,
               hitspeed=2.5,
               speed='Slow'
               )

    G.add_node('RoyalRecruits',
               rarity='Common',
               cost=7,
               count=6,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.3,
               speed='Medium'
               )

    G.add_node('PEKKA',
               rarity='Epic',
               cost=7,
               count=6,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.3,
               speed='Medium'
               )

    G.add_node('LavaHound',
               rarity='Legendary',
               cost=7,
               count=1,
               targets='Buildings',
               flying=True,
               range=3.5,
               hitspeed=1.3,
               speed='Slow'
               )

    G.add_node('MegaKnight',
               rarity='Legendary',
               cost=7,
               count=1,
               targets='Ground',
               flying=False,
               range=2,
               hitspeed=1.7,
               speed='Medium'
               )

    G.add_node('RoyalGiant',
               rarity='Common',
               cost=6,
               count=1,
               targets='Buildings',
               flying=False,
               range=5.0,
               hitspeed=1.7,
               speed='Slow'
               )

    G.add_node('EliteBarbarians',
               rarity='Common',
               cost=6,
               count=2,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.7,
               speed='VeryFast'
               )

    G.add_node('GiantSkeleton',
               rarity='Epic',
               cost=6,
               count=1,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.5,
               speed='Medium'
               )

    G.add_node('GoblinGiant',
               rarity='Epic',
               cost=6,
               count=1,
               targets='Buildings',
               flying=False,
               range=2.0,
               hitspeed=1.7,
               speed='Medium'
               )

    G.add_node('Sparky',
               rarity='Legendary',
               cost=6,
               count=1,
               targets='Ground',
               flying=False,
               range=5.0,
               hitspeed=4.0,
               speed='Slow'
               )

    G.add_node('EliteBarbarians',
               rarity='Common',
               cost=5,
               count=5,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.4,
               speed='Medium'
               )

    G.add_node('MinionHorde',
               rarity='Common',
               cost=5,
               count=6,
               targets='Air&Ground',
               flying=True,
               range=2.0,
               hitspeed=1.0,
               speed='Fast'
               )

    # ISSUES
    G.add_node('Rascals',
               rarity='Common',
               cost=5,
               count=1,
               targets='Air&Ground',
               flying=True,
               range=2.0,
               hitspeed=1.0,
               speed='Medium'
               )

    G.add_node('Balloon',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Buildings',
               flying=True,
               range=2.0,
               hitspeed=3.0,
               speed='Medium'
               )

    G.add_node('Witch',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Air&Ground',
               flying=False,
               range=5.0,
               hitspeed=1.1,
               speed='Medium'
               )

    G.add_node('Prince',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Ground',
               flying=False,
               range=2.0,
               hitspeed=1.4,
               speed='Medium'
               )

    G.add_node('Bowler',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Ground',
               flying=False,
               range=5.0,
               hitspeed=2.5,
               speed='Slow'
               )

    G.add_node('Executioner',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Air&Ground',
               flying=False,
               range=4.5,
               hitspeed=2.4,
               speed='Medium'
               )

    G.add_node('CannonCart',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Ground',
               flying=False,
               range=5.5,
               hitspeed=1.0,
               speed='Fast'
               )

    G.add_node('ElectroDragon',
               rarity='Epic',
               cost=5,
               count=1,
               targets='Air&Ground',
               flying=True,
               range=3.5,
               hitspeed=2.1,
               speed='Medium'
               )

    # ISSUES
    G.add_node('RamRider',
               rarity='Legendary',
               cost=5,
               count=1,
               targets='Buildings',
               flying=False,
               range=1.8,
               hitspeed=1.8,
               speed='Medium'
               )

    return G

