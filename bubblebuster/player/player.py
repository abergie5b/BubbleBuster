from bubblebuster.link import Link, LinkMan
from bubblebuster.settings import DEBUG
from bubblebuster.level import LevelMan, LevelNames
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.scene.scene as sc
import bubblebuster.scene.scenecontext as sccxt

from math import inf
from enum import Enum


class PlayerNames(Enum):
    PLAYERONE = 1
    PLAYERTWO = 2 # ???


class Player(Link):
    def __init__(self, name, weapon, level):
        super().__init__()
        self.name = name
        self.weapon = weapon
        self.level = level
        self.level.player = self

        # stats
        self.stats_bubbles = 0
        self.stats_maxmultiplier = 0
        self.score = 0
        self.stats_explosions = 0
        self.stats_explosionsround = 0
        self.stats_explosionsprev = 0
        self.stats_scoreround = 0
        self.stats_scoreroundprev = 0

    def update(self):
        if self.level.is_complete:
            # update for next level
            self.level.advance()
            # stats
            if self.weapon.ammo and self.weapon.ammo != inf:
                self.score -= self.stats_scoreround
                self.stats_scoreround *= self.weapon.ammo
                self.score += self.stats_scoreround
            if DEBUG:
                print('next level activated %d with %d bubbles and %d max height' % (
                      self.level.level, self.level.bubbles, self.level.bubble_maxh)
                )
                print('scoreround: %d scoreround_raw: %d score %d stats_explosionsround: %d' % (
                      self.stats_scoreround, self.stats_scoreround//self.stats_explosionsround, self.score, self.stats_explosionsround)
                )
            # reset for next level
            self.reset()
            # next scene
            timer.TimerMan.instance.add(timer.SwitchSceneCommand(sc.SceneNames.SCENESWITCH, player=self), 500)
        elif self.level.defeat: # gg
            # stats
            current_time = timer.TimerMan.instance.current_time
            last_collision = sp.ExplosionSprite.instance.last_collision
            # let the current explosion finish and make sure no collisions happening
            if not self.weapon.is_active and current_time - last_collision > self.level.bubble_popdelay:
                if DEBUG:
                    print('game over, switching back to menu current_time: %d last_collision: %d diff: %d' %
                        (current_time, last_collision, current_time - last_collision)
                    )
                # reset player state / statistcs
                self.reset()
                # reset to level 1
                self.level.reset()
                # reset all scenes -> is this necessary?
                sccxt.SceneContext.instance.reset()
                # back to menu
                timer.TimerMan.instance.add(timer.SwitchSceneCommand(sc.SceneNames.MENU), 1000)

    def reset(self):
        # reload and update stats
        self.weapon.reset()
        self.stats_explosionsprev = self.weapon.ammo
        self.stats_scoreroundprev = self.stats_scoreround
        self.stats_scoreround = 0
        self.stats_explosionsround = 0

    def update_max_multiplier(self, multiplier):
        if multiplier and multiplier > self.stats_maxmultiplier:
            self.stats_maxmultiplier = multiplier

    def update_score(self, circle, multiplier=1):
        self.stats_bubbles += 1
        self.update_max_multiplier(multiplier)
        self.level.bubbles -= 1
        points = multiplier * self.level.bubble_maxh//circle.height
        self.score += points
        self.stats_scoreround += points
        if DEBUG:
            print('updating score %d, round: %d circleh: %d mult: %d points: %d bubbles: %d is_complete: %d' % (
                  self.score, self.stats_scoreround, circle.height, multiplier, points, self.level.bubbles, self.level.is_complete)
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
