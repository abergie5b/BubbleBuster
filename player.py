from link import Link, LinkMan
from settings import DEBUG

from enum import Enum


class PlayerNames(Enum):
    PLAYERONE = 1
    PLAYERTWO = 2 # ???


class Player(Link):
    def __init__(self, name, explosions, lives, bubbles):
        super().__init__()
        self.name = name
        self.bubbles = bubbles
        self.explosions = explosions
        self.lives = lives
        self.score = 0

    def update_score(self, circle, multiplier=1):
        self.bubbles -= 1
        points = multiplier * 1000//circle.height
        self.score +=  points
        if DEBUG:
            print('updating player score %d, points: %d' % (self.score, points))
        return points


class PlayerMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not PlayerMan.instance:
            PlayerMan.instance = PlayerMan.__new__(PlayerMan)
            PlayerMan.instance.head = None
        return PlayerMan.instance

    def add(self, player):
        self.base_add(player)
        return player

    def remove(self, player):
        self.base_remove(player)

    def compare(self, a, b):
        return a.name == b or a == b

    def find(self, player):
        return self.base_find(player)
