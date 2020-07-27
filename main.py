import requests
from bs4 import BeautifulSoup


class Card:

    def __init__(self, name):
        self.name = name
        self.weights = {}

    def getMostUsedWith(self):
        return max(self.weights, key=self.weights.get)

    def getUsageWith(self, other):
        if other in self.weights:
            return self.weights[other]
        else:
            return None

    def getMaxWeight(self):
        return max(self.weights.values())

    def getLeastUsedWith(self):
        return min(self.weights, key=self.weights.get)


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
    :return: Nones
    """
    for card in deck:
        if card not in C:
            # add the new Card instance to the dictionary
            C[card] = Card(card)

        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]

        for relatedCard in relatedCards:

            if relatedCard not in C[card].weights:
                C[card].weights[relatedCard] = 1
            else:
                C[card].weights[relatedCard] += 1


def normalize_weights(adjDict):
    w = []
    for card in adjDict:
        w.append(adjDict[card].getMaxWeight())

    normalizer = max(w)

    return adjDict

    # divide all values in adjDict by normalizer





# StatsRoyale urls of grand challenge recent winners and top 200 players
grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='

# RoyaleApi urls
royaleURL = 'https://royaleapi.com/players/leaderboard'

# The 'adjacency dictionary' containing the weights of the links between the cards.
# C[card].weights is the property of the particular Card object we're looking at
# it is a dictionary containing the weights for each other card
C = {}

# Fetch data from ladder
if __name__ == '__main__':

    pagesToParse = 1

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        for deck in get_decks(url):
            link_cards(deck)

    C = normalize_weights(C)