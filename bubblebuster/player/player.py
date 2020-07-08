from bubblebuster.link import Link, LinkMan
from bubblebuster.settings import DEBUG
from bubblebuster.level import LevelMan, LevelNames
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.scene.scene as sc
import bubblebuster.scene.scenecontext as sccxt
import bubblebuster.highscores as hs

from math import inf
from enum import Enum


class PlayerNames(Enum):
    PLAYERONE = 1
    PLAYERTWO = 2 # ???


class Player(Link):
    def __init__(self, name, weapon):
        super().__init__()
        self.name = name
        self.weapon = weapon

        # from input
        self.playername = ''

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
        if LevelMan.instance.current_level.is_complete:
            current_time = timer.TimerMan.instance.current_time
            explosionsprite = sp.ExplosionSprite.instance
            last_collision = explosionsprite.last_collision if explosionsprite else -10000

            # let the current explosion finish and make sure no collisions happening
            if not self.weapon.is_active and current_time - last_collision > LevelMan.instance.current_level.bubble_popdelay:

                # stats
                if self.weapon.ammo and self.weapon.ammo != inf:
                    self.score -= self.stats_scoreround
                    self.stats_scoreround *= self.weapon.ammo
                    self.score += self.stats_scoreround

                # high score
                hs.HighScores.instance.write(self)

                # update for next level
                LevelMan.instance.advance()

                if DEBUG:
                    print('next level activated %d with %d bubbles and %d max height' % (
                          LevelMan.instance.current_level.level, LevelMan.instance.current_level.bubbles, LevelMan.instance.current_level.bubble_maxh)
                    )
                    print('scoreround: %d scoreround_raw: %d score %d stats_explosionsround: %d' % (
                          self.stats_scoreround, self.stats_scoreround//self.stats_explosionsround, self.score, self.stats_explosionsround)
                    )

                # reset for next level
                self.reset()

                # next scene
                timer.TimerMan.instance.add(timer.SwitchSceneCommand(sc.SceneNames.SCENESWITCH), 500)

        elif LevelMan.instance.current_level.defeat: # gg

            # stats
            current_time = timer.TimerMan.instance.current_time
            explosionsprite = sp.ExplosionSprite.instance
            last_collision = explosionsprite.last_collision if explosionsprite else -10000

            # let the current explosion finish and make sure no collisions happening
            if not self.weapon.is_active and current_time - last_collision > LevelMan.instance.current_level.bubble_popdelay:
                if DEBUG:
                    print('game over, switching back to menu current_time: %d last_collision: %d diff: %d' %
                        (current_time, last_collision, current_time - last_collision)
                    )
                # high scores
                hs.HighScores().write(self)

                # reset player state / statistcs
                self.reset()

                # reset to level 1
                LevelMan.instance.reset()

                # reset all scenes -> is this necessary?
                sccxt.SceneContext.instance.reset()

                # back to menu
                timer.SwitchSceneCommand(sc.SceneNames.HIGHSCORES).execute(0)

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
        LevelMan.instance.current_level.bubbles -= 1
        points = multiplier * LevelMan.instance.current_level.bubble_maxh//circle.height
        self.score += points
        self.stats_scoreround += points
        if DEBUG:
            print('updating score %d, round: %d circleh: %d mult: %d points: %d bubbles: %d is_complete: %d' % (
                  self.score, self.stats_scoreround, circle.height, multiplier, points, LevelMan.instance.current_level.bubbles, LevelMan.instance.current_level.is_complete)
            )
        return points


class PlayerMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not PlayerMan.instance:
            PlayerMan.instance = PlayerMan.__new__(PlayerMan)
            PlayerMan.instance.head = None
            PlayerMan.instance.length = 0
        return PlayerMan.instance

    def __init__(self):
        raise NotImplementedError('this is a singleton class')

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

