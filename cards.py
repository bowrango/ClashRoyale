class BabyDragon:

    flying = True
    splash = True

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 113
        self.health = 1024
        self.hs = 1.5
        self.range = 3.5
        self.cost = 4


class Wizard:

    flying = False
    splash = True

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 234
        self.health = 598
        self.hs = 1.4
        self.range = 5.5
        self.cost = 5


class MiniPekka:

    flying = False
    splash = False

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 598
        self.health = 1129
        self.hs = 1.8
        self.range = 1
        self.cost = 4


class MagicArcher:

    flying = False
    splash = True

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 111
        self.health = 490
        self.hs = 1.1
        self.range = 7
        self.cost = 4


class MegaKnight:

    flying = False
    splash = True

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 222
        self.health = 3300
        self.hs = 1.7
        self.range = 1
        self.cost = 7


class Princess:

    flying = False
    splash = True

    def __init__(self, dmg, health, hs, range, cost):

        self.dmg = 140
        self.health = 216
        self.hs = 3
        self.range = 9
        self.cost = 3