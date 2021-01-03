# === Tools for modeling the Clash Royale universe ===

import networkx as nx
import itertools
import requests
from bs4 import BeautifulSoup
import time

import pickle
from networkx.utils import open_file


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


@open_file(1, mode="wb")
def save_graph(G, path, protocol=pickle.HIGHEST_PROTOCOL):
    """Write graph in Python pickle format"""

    pickle.dump(G, path, protocol)


@open_file(0, mode="rb")
def read_graph(path):
    """Read graph in Python pickle format"""
    return pickle.load(path)


# TODO: Use API for this.
def create_card_maps():
    """
    :return: creates mapping dictionaries between each card and its index/url
    """
    base_url = 'https://statsroyale.com/cards'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    card_urls = soup.findAll("div", {"class": "cards__card"})

    valid_urls = []
    cards = []

    for url_result in card_urls:
        card_name = url_result.contents[1].get('href').split('card/')[1]
        card_name = card_name.replace('+', '').replace('-', '').replace('.', '')
        cards.append(card_name)

        valid_urls.append(url_result.contents[1].get('href'))

    card2idx = dict(zip(cards, range(0, len(cards))))
    idx2card = dict(zip(range(0, len(cards)), cards))
    url2map = dict(zip(cards, valid_urls))

    return [card2idx, idx2card, url2map]


# TODO: Use API for this.
def get_node_attributes(card):
    """
    :param card: string of card
    :return: dict containing the key-value attributes for the given card
    """
    url = cardToUrl[card]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    card_attrs = {}
    card_attrs.update({'name': card})

    # Handle certain edge cases where the damage statistics are not included
    if card in ['Lightning', 'Graveyard', 'Poison',
                'RoyalDelivery', 'GoblinBarrel', 'Tornado',
                'Earthquake', 'BarbarianBarrel', 'Mirror',
                'HealSpirit']:

        card_metrics = soup.findAll("div", {"class": "ui__mediumText card__count"})
        for item in card_metrics:
            k = item.parent.contents[1].text
            v = item.text

            # TryCatch error for duplicate keys for attributes we don't want.
            card_attrs.update({k: v})

        return card_attrs

    # TODO: Clean up this logic for getting the correct data table

    hidden_table = soup.find("a", {"class": "ui__mediumText ui__link ui__tab"})
    # If there is only one choice, it's the table we already want
    if hidden_table is None:
        table_stats = soup.find("div", {"class": "statistics__tabContainer", "style": "display: block"})

    # Check which table is the right one
    else:
        if hidden_table.text.replace(" ", "") != card:
            # Take the first table
            table_stats = soup.find("div", {"class": "statistics__tabContainer", "style": "display: block"})
        else:
            # Take the second table
            table_stats = soup.find("div", {"class": "statistics__tabContainer", "style": "display: none"})

    # Base attributes (Targets, Radius, Range, ect.)
    base_attrs = soup.findAll("div", {"class": "ui__mediumText card__count"})

    # TODO: Clean this up
    for attr in base_attrs:
        key = attr.parent.contents[1].text
        val = attr.text

        card_attrs.update({key: val})

    # Damage and health related attributes at max level (Hitpoints, Damage, Damage/sec, ect.)
    maxlvl_stats = table_stats.contents[3].contents[5].contents[-2].text.replace(" ", "")
    maxlvl_stats = maxlvl_stats.split()

    categories = table_stats.contents[3].contents[3].contents[1].text.replace(" ", "")
    categories = categories.split()

    if len(categories) == len(maxlvl_stats):
        attrs = dict(zip(categories, maxlvl_stats))
        card_attrs.update(attrs)

    return card_attrs


def create_empty_graph():
    """
    :return: an empty graph network G with pre-assigned node attributes
    """
    # The graph G is undirected with pre-linked nodes. Each node represents a card and shares a link to all other nodes.

    # - The node attributes establish the nature of the game.
    # - The pre-assigned links represent usages between all cards, which are initialized to 0.
    # - Additional edge attributes will be artificially developed

    # More pushed decks -> better data representation

    # How do we define node attributes to model abilities?, i.e. we cannot hardcode 'drop rage-spell on death'.
    # The attributes should attempt to naturally represent our environment. What are our hyper-parameters?

    # - Explicit: rarity, cost, count, targets, range, hitspeed, speed, health*, damage*
    # - Implicit: flying, placement (regular, any), building

    # *Health and damage depend on card level, but this can be dealt with later. Do we assume stats from max level?

    # Initialize usage links between all nodes
    # G = nx.complete_graph(len(cardToIdx.keys()), )
    # nx.set_edge_attributes(G, 0, 'usages')

    G = nx.empty_graph(len(cardToIdx.keys()))

    # # Testing
    # M = nx.MultiGraph()
    #
    # # All possible 2-pair link combos between N cards
    # combos = itertools.combinations(range(len(cardToIdx.keys())), 2)
    # M.add_edges_from(combos, usages=0)

    # Set node attributes for each card
    for card in cardToIdx.keys():
        n_attrs = get_node_attributes(card)
        n_idx = cardToIdx[card]

        nx.set_node_attributes(G, {n_idx: n_attrs})

        print(f"{card}: {n_idx}")

    return G


cardToIdx, idxToCard, cardToUrl = create_card_maps()
