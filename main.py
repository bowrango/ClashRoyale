import requests
from bs4 import BeautifulSoup


class Card:

    def __init__(self, name):
        self.name = name
        # dictionary containing a weight for each link to another card
        self.links = {}

    def getMostUsedWith(self, count=1):
        return sorted(self.links, key=self.links.get, reverse=true)[:count]

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
        return sum(self.links.values())


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
    :return: None
    """
    for card in deck:
        if card not in C:
            # add the new Card instance to the dictionary
            C[card] = Card(card)

        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]

        for relatedCard in relatedCards:

            if relatedCard not in C[card].links:
                C[card].links[relatedCard] = 1
            else:
                C[card].links[relatedCard] += 1


def normalize_weights(adjdict):
    """
    :param adjdict: the 'adjacency dictionary' which contains all Card instances
    :return: None
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

# 'adjacency dictionary' contains the top-level Card instances
# ex.    obj = C['TheLog'] returns the Card object containing all useful property/method information for TheLog
#        obj.GetMostUsedWith(3) returns the top-3 most used cards with TheLog
C = {}

# Fetch data from ladder
if __name__ == '__main__':

    pagesToParse = 8

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        for deck in get_decks(url):
            link_cards(deck)

    C = normalize_weights(C)

    print(C['Balloon'].getStrength())
    print(C['Bomber'].getStrength())

