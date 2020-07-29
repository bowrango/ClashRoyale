import requests
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
from bs4 import BeautifulSoup

import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go


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


class ChordGraph:

    def __init__(self, player, trophies, result, opponent):
        self.player = player
        self.trophies = trophies
        self.result = result
        self.opponent = opponent


# coverts data for plotting
def map_data(datamatrix, rowvalue, ideogramlength):
    mapped = np.zeros(datamatrix.shape)
    for j in range(L):
        mapped[:, j] = ideogramlength * datamatrix[:, j] / rowvalue
    return mapped


def check_data(data_matrix):
    L, M = data_matrix.shape
    if L != M:
        raise ValueError('Data array must have (n,n) shape')
    return L


def moduloAB(x, a, b):  # maps a real number onto the unit circle identified with

    # the interval [a,b), b-a=2*PI
    if a >= b:
        raise ValueError('Incorrect interval ends')
    y = (x - a) % (b - a)
    return y + b if y < 0 else y + a


def test_2PI(x):
    return 0 <= x < 2 * pi


def get_ideogram_ends(ideogram_len, g):
    ideo_ends = []
    left = 0
    for k in range(len(ideogram_len)):
        right = left + ideogram_len[k]
        ideo_ends.append([left, right])
        left = right + g
    return ideo_ends


def make_ideogram_arc(r, phi, a=50):
    # R is the circle radius
    # phi is the list of ends angle coordinates of an arc
    # a is a parameter that controls the number of points to be evaluated on an arc
    if not test_2PI(phi[0]) or not test_2PI(phi[1]):
        phi = [moduloAB(t, 0, 2 * pi) for t in phi]
    length = (phi[1] - phi[0]) % 2 * pi
    nr = 5 if length <= pi / 4 else int(a * length / pi)

    if phi[0] < phi[1]:
        theta = np.linspace(phi[0], phi[1], nr)
    else:
        phi = [moduloAB(t, -pi, pi) for t in phi]
        theta = np.linspace(phi[0], phi[1], nr)
    return r * np.exp(1j * theta)


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def make_ribbon_ends(mappeddata, ideoends, idxsort):
    L = mappeddata.shape[0]
    ribbonboundary = np.zeros((L, L + 1))
    for k in range(L):
        start = ideoends[k][0]
        ribbonboundary[k][0] = start
        for j in range(1, L + 1):
            J = idxsort[k][j - 1]
            ribbonboundary[k][j] = start + mappeddata[k][J]
            start = ribbonboundary[k][j]
    return [[(ribbonboundary[k][j], ribbonboundary[k][j + 1]) for j in range(L)] for k in range(L)]


def control_pts(angle, radius):
    # angle is a  3-list containing angular coordinates of the control points b0, b1, b2
    # radius is the distance from b1 to the  origin O(0,0)

    if len(angle) != 3:
        raise ValueError('angle must have len =3')
    b_cplx = np.array([np.exp(1j * angle[k]) for k in range(3)])
    b_cplx[1] = radius * b_cplx[1]
    return zip(b_cplx.real, b_cplx.imag)


def ctrl_rib_chords(l, r, radius):
    # this function returns a 2-list containing control poligons of the two quadratic Bezier
    # curves that are opposite sides in a ribbon
    # l (r) the list of angular variables of the ribbon arc ends defining
    # the ribbon starting (ending) arc
    # radius is a common parameter for both control polygons
    if len(l) != 2 or len(r) != 2:
        raise ValueError('the arc ends must be elements in a list of len 2')
    return [control_pts([l[j], (l[j] + r[j]) / 2, r[j]], radius) for j in range(2)]


def make_q_bezier(b):
    # list of its control points
    if len(b) != 3:
        raise ValueError('control poligon must have 3 points')
    A, B, C = b
    return 'M ' + str(A[0]) + ',' + str(A[1]) + ' ' + 'Q ' + \
           str(B[0]) + ', ' + str(B[1]) + ' ' + \
           str(C[0]) + ', ' + str(C[1])


def make_ribbon_arc(theta0, theta1):
    if test_2PI(theta0) and test_2PI(theta1):
        if theta0 < theta1:
            theta0 = moduloAB(theta0, -pi, pi)
            theta1 = moduloAB(theta1, -pi, pi)
            if theta0 * theta1 > 0:
                raise ValueError('incorrect angle coordinates for ribbon')

        nr = int(40 * (theta0 - theta1) / pi)
        if nr <= 2: nr = 3
        theta = np.linspace(theta0, theta1, nr)
        pts = np.exp(1j * theta)

        string_arc = ''
        for k in range(len(theta)):
            string_arc += 'L ' + str(pts.real[k]) + ', ' + str(pts.imag[k]) + ' '
        return string_arc
    else:
        raise ValueError('the angle coordinates for an arc side of a ribbon must be in [0, 2*pi]')


def make_ribbon(l, r, line_color, fill_color, radius=0.2):
    poligon = ctrl_rib_chords(l, r, radius)
    b, c = poligon

    return dict(
        line=dict(
            color=line_color,
            width=0.5
        ),
        path=make_q_bezier(b) + make_ribbon_arc(r[0], r[1]) + make_q_bezier(c[::-1]) + make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def make_layout(title, plot_size):
    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    return go.Layout(title=title,
                     xaxis=dict(axis),
                     yaxis=dict(axis),
                     showlegend=False,
                     width=plot_size,
                     height=plot_size,
                     margin=dict(t=25, b=25, l=25, r=25),
                     hovermode='closest',
                     shapes=[]

                     # to this list one appends below the dicts defining the ribbon,
                     # respectively the ideogram shapes
                     )


def make_ideo_shape(path, line_color, fill_color):
    # line_color is the color of the shape boundary
    # fill_collor is the color assigned to an ideogram
    return dict(
        line=dict(
            color=line_color,
            width=0.45
        ),

        path=path,
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def make_self_rel(l, line_color, fill_color, radius):
    # radius is the radius of Bezier control point b_1
    b = control_pts([l[0], (l[0] + l[1]) / 2, l[1]], radius)
    return dict(
        line=dict(color=line_color, width=0.5),
        path=make_q_bezier(b) + make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def invPerm(perm):
    # function that returns the inverse of a permutation, perm
    inv = [0] * len(perm)
    for i, s in enumerate(perm):
        inv[s] = i
    return inv

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


# increment weights
def link_cards(deck):
    """
    :param deck: a list containing a string for each of the 8 cards
    :return: None
    """
    # Increment the weight for each association
    for card in deck:
        # relatedCards = deck.remove(card)
        relatedCards = [c for c in deck if c != card]
        theseWeights = snapshot[cardToIdx[card]]
        for eachCard in relatedCards:
            theseWeights[cardToIdx[eachCard]] += 1


# normalize data in 2D numpy array
def normalize_weights(array):
    """
    :param array: the 2D 'adjacency matrix' which contains the weights
    :return: the normalized matrix
    """
    # gets max of flattened array
    normalizer = np.amax(array)

    # x -> x/max(x) for all x in array with 0 <= x <= 1
    for idx, weightedArray in enumerate(array):
        array[idx] = np.divide(weightedArray, normalizer)

    return array


# ~~~URLS~~~
grandURL = 'https://statsroyale.com/decks/challenge-winners?type=grand&page='
top200URL = 'https://statsroyale.com/decks/challenge-winners?type=top200&page='
royaleURL = 'https://royaleapi.com/players/leaderboard'

pi = np.pi

# time series data
snapshot = np.zeros((99, 99), dtype=int)

# each card will be mapped to an index in the matrix
cardToIdx = {'Archers': 0,
             'BabyDragon': 1,
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
             'FireSpirits': 19,
             'Fisherman': 20,
             'FlyingMachine': 21,
             'Giant': 22,
             'GiantSkeleton': 23,
             'GoblinCage': 24,
             'GoblinGang': 25,
             'GoblinGiant': 26,
             'Goblins': 27,
             'Golem': 28,
             'Guards': 29,
             'HogRider': 30,
             'Hunter': 31,
             'HealSpirit': 32,
             'IceGolem': 33,
             'IceSpirit': 34,
             'IceWizard': 35,
             'InfernoDragon': 36,
             'Knight': 37,
             'LavaHound': 38,
             'Clone': 39,
             'Lumberjack': 40,
             'MagicArcher': 41,
             'MegaMinion': 42,
             'MegaKnight': 43,
             'MiniPEKKA': 44,
             'Miner': 45,
             'Minions': 46,
             'MinionHorde': 47,
             'Musketeer': 48,
             'NightWitch': 49,
             'PEKKA': 50,
             'Prince': 51,
             'Princess': 52,
             'RamRider': 53,
             'RoyalGhost': 54,
             'RoyalGiant': 55,
             'RoyalHogs': 56,
             'RoyalRecruits': 57,
             'Skeletons': 58,
             'SkeletonArmy': 59,
             'SkeletonBarrel': 60,
             'SkeletonDragons': 61,
             'Sparky': 62,
             'SpearGoblins': 63,
             'ThreeMusketeers': 64,
             'Valkyrie': 65,
             'WallBreakers': 66,
             'Witch': 67,
             'Wizard': 68,
             'Zappies': 69,
             'BombTower': 70,
             'Cannon': 71,
             'InfernoTower': 72,
             'Mortar': 73,
             'Tesla': 74,
             'XBow': 75,
             'BarbarianHut': 76,
             'ElixirCollector': 77,
             'Furnace': 78,
             'GoblinHut': 79,
             'Tombstone': 80,
             'Arrows': 81,
             'BarbarianBarrel': 82,
             'Earthquake': 83,
             'Fireball': 84,
             'Freeze': 85,
             'GiantSnowball': 86,
             'Lightning': 87,
             'Poison': 88,
             'Rocket': 89,
             'RoyalDelivery': 90,
             'TheLog': 91,
             'Tornado': 92,
             'Zap': 93,
             'Rascals': 94,
             'Mirror': 95,
             'Graveyard': 96,
             'Rage': 97,
             'GoblinBarrel': 98
             }

labels = list(cardToIdx.keys())
labelColors = [random_color() for name in labels]

# Fetch data from ladder
if __name__ == '__main__':

    pagesToParse = 1
    decksScraped = 0
    for num in range(1, pagesToParse + 1):
        url = top200URL + str(num)
        for deck in get_decks(url):
            decksScraped += 1
            link_cards(deck)

    snapshot = normalize_weights(snapshot)

    L = check_data(snapshot)
    row_sum = [np.sum(snapshot[k, :]) for k in range(L)]

    # set the gap between two consecutive ideograms
    gap = 2 * pi * 0.005
    ideogram_length = 2 * pi * np.asarray(row_sum) / sum(row_sum) - gap * np.ones(L)

    ideo_ends = get_ideogram_ends(ideogram_length, gap)
    z = make_ideogram_arc(1.3, [11 * pi / 6, pi / 17])

    mapped_data = map_data(snapshot, row_sum, ideogram_length)
    idx_sort = np.argsort(mapped_data, axis=1)
    ribbon_ends = make_ribbon_ends(mapped_data, ideo_ends, idx_sort)
    ribbon_color = [L * [labelColors[k]] for k in range(L)]

    b = [(1, 4), (-0.5, 2.35), (3.745, 1.47)]
    make_q_bezier(b)

    layout = make_layout('Chord diagram', 400)
    radii_sribb = [0.4, 0.30, 0.35, 0.39, 0.12]

    ribbon_info = []
    for k in range(L):

        sigma = idx_sort[k]
        sigma_inv = invPerm(sigma)

        for j in range(k, L):
            if snapshot[k][j] == 0 and snapshot[j][k] == 0:
                continue
            eta = idx_sort[j]
            eta_inv = invPerm(eta)
            l = ribbon_ends[k][sigma_inv[j]]

            if j == k:
                layout['shapes'].append(make_self_rel(l, 'rgb(175,175,175)', labelColors[k], radius=radii_sribb[k]))
                z = 0.9 * np.exp(1j * (l[0] + l[1]) / 2)
                # the text below will be displayed when hovering the mouse over the ribbon
                text = labels[k] + ' commented on ' + '{:d}'.format(snapshot[k][k]) + ' of ' + 'herself Fb posts',
                ribbon_info.append(go.Scatter(x=[z.real],
                                              y=[z.imag],
                                              mode='markers',
                                              marker=dict(size=0.5, color=labelColors[k]),
                                              text=text,
                                              hoverinfo='text'
                                              )
                                   )

            else:
                r = ribbon_ends[j][eta_inv[k]]
                zi = 0.9 * np.exp(1j * (l[0] + l[1]) / 2)
                zf = 0.9 * np.exp(1j * (r[0] + r[1]) / 2)
                texti = labels[k] + ' commented on ' + '{:d}'.format(snapshot[k][j]) + ' of ' + labels[j] + ' Fb posts'
                textf = labels[j] + ' commented on ' + '{:d}'.format(snapshot[j][k]) + ' of ' + labels[k] + ' Fb posts'
                ribbon_info.append(go.Scatter(x=[zi.real],
                                              y=[zi.imag],
                                              mode='markers',
                                              marker=dict(size=0.5, color=ribbon_color[k][j]),
                                              text=texti,
                                              hoverinfo='text'
                                              )
                                   ),
                ribbon_info.append(go.Scatter(x=[zf.real],
                                              y=[zf.imag],
                                              mode='markers',
                                              marker=dict(size=0.5, color=ribbon_color[k][j]),
                                              text=textf,
                                              hoverinfo='text'
                                              )
                                   )
                r = (r[1], r[0])  # IMPORTANT!!!  Reverse these arc ends because otherwise you get
                # a twisted ribbon
                # append the ribbon shape
                print(layout['shapes'])
                # layout['shapes'].append(make_ribbon(l, r, 'rgb(175,175,175)', ribbon_color[k][j]))

    ideograms = []
    for k in range(len(ideo_ends)):
        z = make_ideogram_arc(1.1, ideo_ends[k])
        zi = make_ideogram_arc(1.0, ideo_ends[k])
        m = len(z)
        n = len(zi)
        ideograms.append(go.Scatter(x=z.real,
                                    y=z.imag,
                                    mode='lines',
                                    line=dict(color=labelColors[k], shape='spline', width=0.25),
                                    text=labels[k] + '<br>' + '{:d}'.format(row_sum[k]),
                                    hoverinfo='text'
                                    )
                         )

        path = 'M '
        for s in range(m):
            path += str(z.real[s]) + ', ' + str(z.imag[s]) + ' L '

        Zi = np.array(zi.tolist()[::-1])

        for s in range(m):
            path += str(Zi.real[s]) + ', ' + str(Zi.imag[s]) + ' L '
        path += str(z.real[0]) + ' ,' + str(z.imag[0])

        layout['shapes'].append(make_ideo_shape(path, 'rgb(150,150,150)', labelColors[k]))

    data = go.dict(ideograms + ribbon_info)
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='chord-diagram-Fb')

    # plot the weights
    # plt.imshow(snapshot, cmap='hot', interpolation='nearest')
    # plt.title(decksScraped)
    # plt.show()
    # print(decksScraped)
