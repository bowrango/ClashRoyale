import requests
import numpy as np
from bs4 import BeautifulSoup


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


# don't need now
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


# retrieve data
def get_decks(url):
    """
    :param url: page containing HTMl deck data
    :return collection: a list containing a list for each deck used
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    decksUsed = soup.findAll("div", {"class": "recentWinners__decklist"})

    collection = []

    for deck in decksUsed:
        allCards = deck.findChildren('a', recursive=False)

        deckSet = []

        for card in allCards:
            # format card names
            cardString = card.get('href').split('card/')[1]
            cardString = cardString.replace('+', '').replace('-', '').replace('.', '')

            deckSet.append(cardString)

        collection.append(deckSet)

    return collection


def link_cards(deck):
    """
    :param deck: a list containing a string for each of the 8 cards
    :return: a np array of the current meta, i.e. the weighted matrix
    """

    # CONVERT THIS WHOLE FUNCTION TO BUILDING THE NXN MATRIX AS A NP ARRAY

    for card in deck:
        if card not in C:
            # add the new Card instance to the dictionary
            C[card] = Card(card)

        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]

        for relatedCard in relatedCards:

            # M = {wij}, the adjacency matrix describing the weights within current meta
            # using symmetric positive weights wij = wji > 0, with no loops wii = 0

            if relatedCard not in C[card].links:
                C[card].links[relatedCard] = 1
            else:
                C[card].links[relatedCard] += 1


# PUT THIS INTO LINK_CARDS
def normalize_weights(adjdict):
    """
    :param adjdict: the 'adjacency dictionary' which contains all Card instances
    :return: NonE
    """

    w = []
    # get max weight
    for card in adjdict:
        w.append(adjdict[card].getMaxWeight())

    normalizer = max(w)

    # divide all values by this weight
    for card in adjdict:
        adjdict[card].links = {key: round(value/normalizer, 3) for key, value in adjdict[card].links.items()}

    return adjdict


# ~~~URLS~~~
grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='
royaleURL = 'https://royaleapi.com/players/leaderboard'

C = {}

# time series data
snapshot = np.zeros((99, 99))

# each card will be mapped an index into this matrix...ugh
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
             'RoyalHog': 56,
             'RoyalRecruit': 57,
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
             'Goblin Hut': 79,
             'Goblin Cage': 80,
             'Tombstone': 81,
             'Arrows': 82,
             'BarbarianBarrel': 83,
             'Earthquake': 84,
             'Fireball': 85,
             'Freeze': 86,
             'GiantSnowball': 87,
             'Lightning': 88,
             'Poison': 89,
             'Rocket': 90,
             'RoyalDelivery': 91,
             'TheLog': 92,
             'Tornado': 93,
             'Zap': 94,
             'Rascals': 95,
             'EarthQuake': 96,
             'Mirror': 97,
             'Graveyard': 98,
             'Rage': 99
             }

# Fetch data from ladder
if __name__ == '__main__':

    pagesToParse = 1

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        for deck in get_decks(url):
            link_cards(deck)

    C = normalize_weights(C)

    print(C['Balloon'].getStrength())

