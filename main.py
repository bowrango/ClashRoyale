import requests
import cards
from bs4 import BeautifulSoup

url = 'https://statsroyale.com/decks/challenge-winners?type=grand&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
allDecks = soup.findAll("div", {"class": "recentWinners__decklist"})

for deck in allDecks:
    print('new deck')
    cards = deck.findChildren('a', recursive=False)
    for card in cards:
        cardString = card.get('href')
        print(type(cardString))
    print('-------')