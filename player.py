from link import Link, LinkMan
from settings import DEBUG
import scene

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
        self.current_level = 1
        self.score = 0

    def update(self):
        if self.explosions <= 0:
            scene.SceneContext.instance.reset()
            scene.SceneContext.instance.set_state(scene.SceneNames.MENU)

    def update_score(self, circle, multiplier=1):
        self.bubbles -= 1
        points = multiplier * 1000//circle.height
        self.score +=  points
        if DEBUG:
            print('updating score %d, circleh: %d mult: %d points: %d bubbles: %d' % (
                  self.score, circle.height, multiplier, points, self.bubbles)
            )
        return points


class PlayerMan(LinkMan):

    def add(self, player):
        self.base_add(player)
        return player

    def remove(self, player):
        self.base_remove(player)

    def compare(self, a, b):
        return a.name == b or a == b

    def find(self, player):
        return self.base_find(player)

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next

    @staticmethod
    def set_active(manager):
        PlayerMan.instance = manager
