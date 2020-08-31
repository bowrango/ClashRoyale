
import networkx as nx
import meta_fetching as mf
import meta_visualization as mv

import time

# Each card will be mapped to an index in the matrix
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

# Labels for chord graph
labels = list(cardToIdx.keys())

# Fetch data from ladder
if __name__ == '__main__':

    t0 = time.perf_counter()

    # Specify how many decks a graph should be representative of
    G1 = mf.build_graph(decks=15)
    # G2 = mf.build_graph(decks=10)
    # G3 = mf.build_graph(decks=100)
    # G4 = mf.build_graph(decks=1000)

    t1 = time.perf_counter()
    print(f"Build Time: {round(t1-t0, 5)}")

    # A complete graph has a density of 1.
    # An empty graph with no connected nodes has a density of 0
    print(nx.density(G1))
    # print(nx.density(G2))
    # print(nx.density(G3))
    # print(nx.density(G4))






