# === Tools for receiving data about the Clash Royale universe ===

import meta_handling as mh
from meta_handling import cardToIdx
from meta_handling import combos8

import requests
from bs4 import BeautifulSoup
import itertools

from PIL import Image

# retrieves deck usage data
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
    filename = card_str+'.png'
    # If the file already exists, who cares? Just re-save it
    image.save(path+filename)
    print('Image of '+card_str+' saved!')


def push_deck(deck, graph):
    """
    :param graph: parent networkx graph object to be updated
    :param deck: a list containing a string for each of the 8 cards
    :return: None
    """

    # updates edges between pairs
    for (u, v) in combos8:

        this_card, other_card = deck[u], deck[v]
        this_graph_idx, other_graph_idx = cardToIdx[this_card], cardToIdx[other_card]

        graph[this_graph_idx][other_graph_idx]['usages'] += 1

    # increment the weight for each association
    # for idx, node in enumerate(deck):
    #
    #     this_node_idx = cardToIdx[node]
    #     # other_nodes = deck[idx+1:]
    #     # other_nodes = deck.remove(node)
    #     other_nodes = [n for n in deck if n != node]
    #
    #     for each_node in other_nodes:
    #         other_node_idx = cardToIdx[each_node]
    #         graph[this_node_idx][other_node_idx]['usages'] += 1


# creates a new network graph from recent data
def build_graph(decks=None, Top200=True):

    # create an empty graph network with all assigned node attributes
    if decks is None:
        return mh.create_empty_graph()
    else:
        G = mh.create_empty_graph()
        n = 0

    # Ugly
    if Top200:
        url = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='
    else:
        url = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='

    page = 1
    while n < decks:

        url = url + str(page)
        for deck in get_decks(url, save_imgs=False):
            n += 1
            if n == decks:
                break
            push_deck(deck, G)
        page += 1
    print(f"Decks Used: {n}")
    return G

