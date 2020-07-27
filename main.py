import requests
import datetime
import numpy as np
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
        return round(sum(self.links.values()), 3)


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
    :return: a np array of the current meta, i.e. the weighted matrix
    """

    # CONVERT THIS WHOLE FUNCTION TO BUILDING THE NXN MATRIX AS A NP ARRAY

    for card in deck:
        if card not in C:
            # add the new Card instance to the dictionary
            C[card] = Card(card)

        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]

        for relatedCard in relatedCards:

            # M = {wij}, the adjacency matrix describing the weights within current meta
            # using symmetric positive weights wij = wji > 0, with no loops wii = 0

            if relatedCard not in C[card].links:
                C[card].links[relatedCard] = 1
            else:
                C[card].links[relatedCard] += 1


# PUT THIS INTO LINK_CARDS
def normalize_weights(adjdict):
    """
    :param adjdict: the 'adjacency dictionary' which contains all Card instances
    :return: NonE
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

# time series data
snapshot = np.zeros((99, 99))

# each card will be mapped an index into this matrix...ugh
cardToIdx = {'Archers': 0,
             'BabyDragon' : 1,
             'Balloon': 2,
             'Bandit': 3,
             'Barbarians': 4,
             'Bats': 5,
             'BattleHealer': 6,
             'BattleRam': 7,
             'Bomber': 8,
             'Bowler': 9,
             'CannonCart': 10,
             'DarkPrince': 11,
             'DartGoblin': 12,
             'ElectroDragon': 13,
             'ElectroWizard': 14,
             'EliteBarbarians': 15,
             'ElixirGolem': 16,
             'Executioner': 17,
             'Firecracker': 18,
             'Fire Spirits': 19,
             'Fisherman': 20,
             'Flying Machine': 21,
             'Giant': 22,
Giant Skeleton
Goblin Brawler
Goblin Gang	3	167/110	99/67	1.1/1.7	90/39	0/0	0.5 (Melee: Short)/5	3/2
Goblin Giant	6	2,540	146	1.7	85	0	1.2 (Melee: Medium)	1
Goblins	2	167	99	1.1	90	0	0.5 (Melee: Short)	3
Golem	8	4,256	259	2.5	103	259 (Death)	0.75 (Melee: Short)	1
Golemite	N/A	864	53	2.5	21	53 (Death)	0.25 (Melee: Short)	2
Guards	3	90 (+199)	90	1.1	81	0	1.6 (Melee: Long)	3
Hog Rider	4	1,408	264	1.6	165	0	0.8 (Melee: Short)	1
Hunter	4	696	69 (x10)	2.2	31 (x10)	0	4	1
Heal Spirit	1	191	91	N/A	N/A	0	2.5	1
Ice Golem	2	994	70	2.5	28	70 (Death)	0.75 (Melee: Short)	1
Ice Spirit	1	190	91	N/A	N/A	0	2.5	1
Ice Wizard	3	590	75	1.7	40	0	5.5	1
Inferno Dragon	4	1,070	30-350	0.4	75-875	0	3.5	1
Knight	3	1,452	167	1.2	139	0	1.2 (Melee: Medium)	1
Lava Hound	7	3,150	45	1.3	34	0	3.5	1
Lava Pup	N/A	179	75	1.7	44	0	1.6 (Melee: Long)	6
Lumberjack	4	1,060	200	0.8	250	0	0.7 (Melee: Short)	1
Magic Archer	4	440	111	1.1	100	0	7	1
Mega Minion	3	695	258	1.6	161	0	1.6 (Melee: Long)	1
Mega Knight	7	3,300	222	1.7	123	444 (Spawn)	1.2 (Melee: Medium)	1
Mini P.E.K.K.A.	4	1,129	598	1.8	332	0	0.8 (Melee: Short)	1
Miner	3	1,000	160	1.2	133	0	1.2 (Melee: Medium)	1
Minions	3	190	84	1	84	0	1.6 (Melee: Long)	3
Minion Horde	5	190	84	1	84	0	1.6 (Melee: Long)	6
Musketeer	4	598	181	1.1	164	0	6	1
Night Witch	4	750	260	1.5	173	0	1.6 (Melee: Long)	1
P.E.K.K.A.	7	3,125	678	1.8	376	0	1.2 (Melee: Medium)	1
Prince	5	1,669	325	1.4	232	0	1.6 (Melee: Long)	1
Princess	3	216	140	3	46	0	9	1
Ram Rider	5	1,461	220/86	1.8/1.1	122/78	0	0.8 (Melee: Short)/5.5	1
Rascal Boy	5	1,515	110	1.5	73	0	0.8 (Melee: Short)	1
Rascal Girl	5	216	110	1.1	100	0	5	2
Royal Ghost	3	1,000	216	1.8	120	0	1.2 (Melee: Medium)	1
Royal Giant	6	2,544	254	1.7	149	0	5	1
Royal Hogs
Royal Recruits
Skeletons
Skeleton Army
Skeleton Barrel
Skeleton Dragons
Sparky
Spear Goblins
Three Musketeers
Valkyrie
Wall Breakers
Witch
Wizard
Zappies




             }

# Fetch data from ladder
if __name__ == '__main__':

    pagesToParse = 1
    time = datetime.now()

    for num in range(1, pagesToParse+1):
        url = top200URL+str(num)
        for deck in get_decks(url):
            link_cards(deck)

    C = normalize_weights(C)

    metadata = np.array()

    print(C['Balloon'].getStrength())
    print(C['Bomber'].getStrength())

