import requests
import urllib.request
import time
import cards
from bs4 import BeautifulSoup

url = 'https://statsroyale.com/decks/challenge-winners?type=grand&page=1'

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
