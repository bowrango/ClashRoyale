# === Tools for receiving data about the Clash Royale universe ===

from meta_handling import cardToIdx

import itertools
import time

import clashroyale as cr

# official API Developer token, this should be private
key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkwMDJiMWE3LTRhMTItNDdhMy04MDU2LTU5YmFiZTZmZmVjZiIsImlhdCI6MTYwOTE5Njc3Mywic3ViIjoiZGV2ZWxvcGVyL2MyMGJhNThjLTlkNGUtMDFkZC01YzUwLTI5ZDMzZDZlMDNjNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.1RKFtdown15NHs9gv32_25jsS2iS7uhrrM0Q2RjRTWNwVAYVwe9Q3FvscLn20DZU9ZhvJ_1vziLATz98JrzShg'
proxy_url = 'https://proxy.royaleapi.dev/v1'


# updates a graph with new deck information
def push_deck(deck, G):
    """
    :param G: parent networkx graph object to be updated
    :param deck: a list containing a string for each of the 8 cards
    :return: the updated graph
    """
    # all 28 possible 2-pair edge combos for an 8 card deck
    combos = itertools.combinations(range(len(deck)), 2)

    # TODO: Optimize this
    for (u, v) in combos:
        u_idx, v_idx = cardToIdx[deck[u]], cardToIdx[deck[v]]

        if G.has_edge(u_idx, v_idx):
            G[u_idx][v_idx]['usages'] += 1
        else:
            G.add_edge(u_idx, v_idx, usages=1)

    return G


def format_card_string(card_string):
    card_string = card_string.replace(' ', '').replace('-', '').replace('.', '')
    return card_string


def build_graph(G, rank=100):

    t0 = time.perf_counter()
    G.Rank = rank

    # Consider assigning the client to the graph?

    client = cr.official_api.Client(token=key, url=proxy_url)
    top_players = client.get_top_players(limit=rank)
    top_players = top_players.raw_data

    # go through and get the current deck for each player
    p = 1
    for player in top_players:
        tag = player['tag']
        player_info = client.get_player(tag)
        current_deck = player_info.raw_data['currentDeck']

        # format into list of strings
        current_deck = [format_card_string(dict_idx['name']) for dict_idx in current_deck]
        G = push_deck(current_deck, G)

        print(f"{p} / {rank}")
        p = p + 1

    t1 = time.perf_counter()
    print(f"Build Time: {t1 - t0}")
    return G
