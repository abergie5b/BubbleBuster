import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.scene.scene as sc
import bubblebuster.scene.scenecontext as sccxt
import bubblebuster.highscores as hs
from bubblebuster.link import Link, LinkMan
from bubblebuster.settings import DEBUG
import bubblebuster.level as le

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
        self.stats_bubblesround = 0
        self.stats_maxmultiplier = 0
        self.stats_maxmultiplierround = 0
        self.score = 0
        self.stats_explosions = 0
        self.stats_explosionsround = 0
        self.stats_explosionsprev = 0
        self.stats_scoreround = 0
        self.stats_scoreroundprev = 0

    def update(self):
        if le.LevelMan.instance.current_level.is_complete:
            current_time = timer.TimerMan.instance.current_time
            explosionsprite = sp.ExplosionSprite.instance
            last_collision = explosionsprite.last_collision if explosionsprite else -10000

            # let the current explosion finish and make sure no collisions happening
            if not self.weapon.is_active and current_time - last_collision > le.LevelMan.instance.current_level.bubble_popdelay:

                # stats
                if self.weapon.ammo and self.weapon.ammo != inf:
                    self.score -= self.stats_scoreround
                    self.stats_scoreround *= self.weapon.ammo
                    self.score += self.stats_scoreround

                # high score
                hs.HighScores.instance.write(self)

                # update for next level
                le.LevelMan.instance.advance()

                if DEBUG:
                    print('next level %s activated %d with %d target_bubbles %d bubbles %d max height' % (
                          le.LevelMan.instance.current_level.name.name, le.LevelMan.instance.current_level.level, le.LevelMan.instance.current_level.target_bubbles, le.LevelMan.instance.current_level.bubbles, le.LevelMan.instance.current_level.bubble_maxh)
                    )
                    # div by zero (this still happens)
                    print('scoreround: %d scoreround_raw: %d score %d stats_explosionsround: %d' % (
                          self.stats_scoreround, self.stats_scoreround//self.stats_explosionsround, self.score, self.stats_explosionsround)
                    )

                # reset for next level
                self.reset()

                # next scene
                timer.SwitchSceneCommand(sc.SceneNames.SCENESWITCH).execute(0)

        elif le.LevelMan.instance.current_level.defeat: # gg

            # stats
            current_time = timer.TimerMan.instance.current_time
            explosionsprite = sp.ExplosionSprite.instance
            last_collision = explosionsprite.last_collision if explosionsprite else -10000

            # let the current explosion finish and make sure no collisions happening
            if not self.weapon.is_active and current_time - last_collision > le.LevelMan.instance.current_level.bubble_popdelay:
                if DEBUG:
                    print('game over, switching back to menu current_time: %d last_collision: %d diff: %d' %
                        (current_time, last_collision, current_time - last_collision)
                    )
                    
                # high scores
                hs.HighScores().write(self)

                # reset player state / statistcs
                self.reset()

                # reset all levels
                le.LevelMan.instance.init()

                # reset all scenes -> is this necessary?
                sccxt.SceneContext.instance.reset()

                # back to menu
                timer.SwitchSceneCommand(sc.SceneNames.HIGHSCORES).execute(0)

    def reset(self):
        if DEBUG:
            print('reseting player %s and weapon %s' % (self.name, self.weapon))
        # reload and update stats
        if self.weapon:
            self.weapon.reset()
            self.stats_explosionsprev = self.weapon.ammo
        self.stats_scoreroundprev = self.stats_scoreround
        self.stats_bubblesround = 0
        self.stats_scoreround = 0
        self.stats_explosionsround = 0
        self.stats_maxmultiplierround = 0

    def update_maxmultiplier(self, multiplier, maxmultiplier):
        if multiplier and multiplier > getattr(self, maxmultiplier):
            setattr(self, maxmultiplier, multiplier)

    def update_score(self, circle, multiplier=1):
        self.stats_bubbles += 1
        self.stats_bubblesround += 1
        self.update_maxmultiplier(multiplier, 'stats_maxmultiplier')
        self.update_maxmultiplier(multiplier, 'stats_maxmultiplierround')
        le.LevelMan.instance.current_level.target_bubbles -= 1
        le.LevelMan.instance.current_level.bubbles -= 1
        points = multiplier * le.LevelMan.instance.current_level.bubble_maxh//circle.height
        self.score += points
        self.stats_scoreround += points
        if DEBUG:
            print('updating score %d, round: %d circleh: %d mult: %d points: %d explosionsround: %d bubblesround: %d is_complete: %d' % (
                  self.score, self.stats_scoreround, circle.height, multiplier, points, self.stats_explosionsround, self.stats_bubbles, le.LevelMan.instance.current_level.is_complete)
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

