import requests
import cards
import re
import pickle
import os
from bs4 import BeautifulSoup


def get_decks(url):
    """
    :param url: page containing the most recent decks used by the winning top 200 players
    :return: a list for each deck on the page containing the strings of the cards used
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    decksUsed = soup.findAll("div", {"class": "recentWinners__decklist"})

    for deck in decksUsed:
        allCards = deck.findChildren('a', recursive=False)

        deckSet = []

        for card in allCards:
            # format card names
            cardString = card.get('href').split('card/')[1]
            cardString = cardString.replace('+', '').replace('-', '').replace('.', '')

            deckSet.append(cardString)

        print(deckSet)


if __name__ == '__main__':

    pagesToParse = 1
    # URLs of grand challenge recent winners and top 200 players
    grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
    top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        get_decks(url)

