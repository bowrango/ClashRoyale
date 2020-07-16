import requests
import cards
import pickle
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

    def getLeastUsedWith(self):
        return min(self.weights, key=self.weights.get)


class Deck:

    # add some persistent variable here
    def __init(self, player, trophies, result, opponent):

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


def map_cards(deck):
    """
    :param deck: a list containing a string for each of the 8 cards
    :return: Nones
    """
    for card in deck:
        if card not in cards:
            # add a new Card instance to the dictionary
            cards[card] = Card(card)

        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]

        for relatedCard in relatedCards:

            # cards[card].weights is the property of the particular Card object we're looking at
            # it is a dictionary containing the weights for each other card

            if relatedCard not in cards[card].weights:
                cards[card].weights[relatedCard] = 1
            else:
                cards[card].weights[relatedCard] += 1


cards = {}
PlayerDecks = {}

if __name__ == '__main__':

    pagesToParse = 1
    # Urls of grand challenge recent winners and top 200 players
    grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
    top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        for deck in get_decks(url):
            map_cards(deck)

    print(cards['Miner'].getMostUsedWith())