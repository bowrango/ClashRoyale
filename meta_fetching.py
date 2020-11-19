# === Tools for receiving data about the Clash Royale universe ===

import meta_handling as mh
from meta_handling import cardToIdx

import requests
from bs4 import BeautifulSoup
import itertools

from PIL import Image
import time

import networkx as nx
import matplotlib.pyplot as plt


# retrieves deck usage data

# TODO: move the save image capability to meta_handling. The card_urls within create_card_maps() already contain the src
def get_decks(url, save_imgs=False):
    """
    :param save_imgs: scrape and save all card images to a folder
    :param url: page containing HTMl deck data
    :return collection: a list containing a list for each deck used
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    decksUsed = soup.findAll("div", {"class": "recentWinners__decklist"})
    # timeStamps = soup.findAll("div", {"class": "ui__smallText ui__greyText"})
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


# save card images to a folder
def save_image(image, card_str):
    """
    :param image: the PIL Image object
    :param card_str: name of the card
    :return: None
    """
    path = 'C:/Users/Matt/PycharmProjects/ClashRoyale/images/'
    filename = card_str + '.png'
    # If the file already exists, who cares? Just re-save it
    image.save(path + filename)
    print('Image of ' + card_str + ' saved!')


# updates a graph with new deck information
def push_deck(deck, G):
    """
    :param G: parent networkx graph object to be updated
    :param deck: a list containing a string for each of the 8 cards
    :return: the updated graph
    """
    # updates all 28 possible 2-pair edge combos
    combos = itertools.combinations(range(len(deck)), 2)

    # TODO: Optimize this
    for (u, v) in combos:
        this_card, other_card = deck[u], deck[v]
        this_graph_idx, other_graph_idx = cardToIdx[this_card], cardToIdx[other_card]

        G[this_graph_idx][other_graph_idx]['usages'] += 1

    return G


# creates a new network graph from recent data
def build_graph(G, decks=None, Top200=True, animate=False):
    """
    :param animate: show the deck updates frame by frame
    :param G: the networkx graph to be updated
    :param decks: how many decks the graph should be representative of
    :param Top200: True for Top 200, False for Grand Challenge Winners
    :return: the updated graph network
    """

    # Tag the graph with the number of decks it is representative of
    G.decks = decks

    # Ugly
    if Top200:
        url = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='
    else:
        url = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='

    page = 1
    n = 0
    t0 = time.perf_counter()
    while n < decks:
        url = f"{url}{page}"
        for deck in get_decks(url, save_imgs=False):
            if n == decks:
                t1 = time.perf_counter()
                print(f"Build Time: {t1 - t0}")
                print(f"Decks Used: {n}")
                return G
            n += 1
            G = push_deck(deck, G)
            if animate is True:
                m = nx.convert_matrix.to_numpy_array(G, weight='usages')
                plt.imshow(m, cmap='hot')
                plt.show()
                plt.close()

        page += 1

    t1 = time.perf_counter()
    print(f"Build Time: {t1-t0}")
    print(f"Decks Used: {n}")
    return G
