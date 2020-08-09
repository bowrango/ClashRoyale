import requests
from bs4 import BeautifulSoup

import networkx as nx

import PIL
from PIL import Image
import os.path

import numpy as np

import pickle

from matplotlib import pyplot as plt


from chord import Chord


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

# retrieves useful data
def get_decks(url, save_imgs=False):
    """
    :param save_imgs: scrape and save all card images to a folder
    :param url: page containing HTMl deck data
    :return collection: a list containing a list for each deck used
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    decksUsed = soup.findAll("div", {"class": "recentWinners__decklist"})
    timeStamps = soup.findAll("div", {"class": "ui__smallText ui__greyText"})

    # times = [str(ts.contents[0]) for ts in timeStamps]

    collection = []

    for deck in decksUsed:

        allCards = deck.findChildren('a', recursive=False)
        deckSet = []

        for card in allCards:
            # format card names
            cardString = card.get('href').split('card/')[1]
            cardString = cardString.replace('+', '').replace('-', '').replace('.', '')
            deckSet.append(cardString)

            if save_imgs:
                # path to card image
                img_path = card.contents[1].get('src')
                img = Image.open(requests.get(img_path, stream=True).raw)
                save_image(img, cardString)

        collection.append(deckSet)

    return collection


# saves card images to a folder
def save_image(image, card_str):
    """
    :param image: the PIL Image object
    :param card_str: name of the card
    :return: None
    """
    path = 'C:/Users/Matt/PycharmProjects/ClashRoyale/images/'
    filename = card_str+'.png'
    # If the file already exists, who cares? Just re-save it
    image.save(path+filename)
    print('Image of '+card_str+' saved!')


# increments weights
def link_cards(deck):
    """
    :param deck: a list containing a string for each of the 8 cards
    :return: None
    """
    # Increment the weight for each association
    for card in deck:
        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]
        theseWeights = snapshot[cardToIdx[card]]
        for eachCard in relatedCards:

            # Networkx implementation
            if G.has_edge(card, eachCard):
                G[card][eachCard]['weight'] += 1
            else:
                G.add_edge(card, eachCard, weight=1)

            # Me
            theseWeights[cardToIdx[eachCard]] += 1


# normalizes data in the 2D numpy array
def normalize_weights(array):
    """
    :param array: the 2D 'adjacency matrix' which contains the weights
    :return: the normalized matrix, along its maximums
    """
    # gets max of flattened array
    normalizer = np.amax(array)

    # x -> x/max(x) for all x in array with 0 <= x <= 1
    for idx, weightedArray in enumerate(array):
        array[idx] = np.true_divide(weightedArray, normalizer)

    return array, normalizer


# ~~~URLS~~~
grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='
royaleURL = 'https://royaleapi.com/players/leaderboard'

# retrieve time series array of the weighted matrices
# f = open('meta.pckl', 'rb')
# gameplay = pickle.load(f)
# f.close()

# stacked list of 10 initialized 99x99 weighted adjacency matrices
gameplay = np.zeros(shape=(10, 99, 99))

# initialize undirected and weighted matrix
snapshot = np.zeros((99, 99), dtype=float)

# each card will be mapped to an index in the matrix
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

# Let's try and implement a networkx graph
G = nx.Graph()

# Fetch data from ladder
if __name__ == '__main__':

    # essentially indicates how precise the time series data is. The matrix is normalized after parsing all
    # the pages, then added the matrix.
    pagesToParse = 1
    decksScraped = 0


    for num in range(pagesToParse+1):
        url = top200URL + str(num)
        for deck in get_decks(url, save_imgs=False):
            decksScraped += 1
            link_cards(deck)
    snapshot, norm = normalize_weights(snapshot)


    # just overwrite the first matrix for now
    gameplay[0] = snapshot

    f = open('meta.pckl', 'wb')
    pickle.dump(gameplay, f)

    # Chord(snapshot, labels).to_html()

    # plot the weights
    title = 'd = ' + str(decksScraped) + ', norm = ' + str(norm)
    plt.imshow(snapshot, cmap='hot', interpolation='nearest')
    plt.title(title)

    print(nx.number_of_nodes(G))

    # A list of frequencies of degrees. The degree values are the index in the list.
    print(nx.degree_histogram(G))
    for e in nx.all_neighbors(G, 'Zap'):
        print(e)

