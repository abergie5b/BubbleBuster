import bubblebuster.timer as timer
from bubblebuster.link import Link, LinkMan
from bubblebuster.settings import DEBUG, GameSettings
import bubblebuster.sprite as sp
import bubblebuster.scene as scene

from enum import Enum


class PlayerNames(Enum):
    PLAYERONE = 1
    PLAYERTWO = 2 # ???


class Player(Link):
    def __init__(self, name, explosions, bubbles):
        super().__init__()
        self.name = name
        self.bubbles = bubbles
        self.explosions = explosions
        self.current_level = 1

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
        if self.bubbles <= 0:
            # update for next level
            self.current_level += 1
            GameSettings.NUMBER_OF_BUBBLES += 5
            GameSettings.BUBBLE_MAXH -= 10
            # stats
            if self.explosions:
                self.score -= self.stats_scoreround
                self.stats_scoreround *= self.explosions
                self.score += self.stats_scoreround
            # reset for next level
            if DEBUG:
                print('next level activated %d with %d bubbles and %d max height' % (self.current_level, self.bubbles, GameSettings.BUBBLE_MAXH))
                print('scoreround: %d scoreround_raw: %d score %d stats_explosionsround: %d' % (self.stats_scoreround, self.stats_scoreround//self.stats_explosionsround, self.score, self.stats_explosionsround))
            self.reset()
            # next level
            #scene.SceneContext.instance.set_state(scene.SceneNames.SCENESWITCH, self)
            timer.TimerMan.instance.add(timer.SwitchSceneCommand(scene.SceneNames.SCENESWITCH, player=self), 1000)
        elif self.explosions <= 0: 
            current_time = timer.TimerMan.instance.current_time
            last_collision = sp.ExplosionSprite.instance.last_collision
            # this depends how long it takes for the explosions
            # GameSettings.EXPLOSION_MAX_LIVES is not exactly frame by frame
            # and not measured in time
            # so better to make it large just in case
            totally_random_number = 100
            if current_time - last_collision > GameSettings.BUBBLEPOPDELAY + GameSettings.EXPLOSION_MAX_LIVES * totally_random_number:
                if DEBUG:
                    print('game over, switching back to menu current_time: %d last_collision: %d diff: %d' %
                        (current_time, last_collision, current_time - last_collision))
                self.reset()
                GameSettings.init()
                scene.SceneContext.instance.reset()
                # die
                timer.TimerMan.instance.add(timer.SwitchSceneCommand(scene.SceneNames.MENU), 1000)

    def reset(self):
        # reset these or something
        self.bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.stats_explosionsprev = self.explosions
        self.explosions = GameSettings.PLAYER_EXPLOSIONS
        self.stats_scoreroundprev = self.stats_scoreround
        self.stats_scoreround = 0
        self.stats_explosionsround = 0

    def update_max_multiplier(self, multiplier):
        if multiplier and multiplier > self.stats_maxmultiplier:
            self.stats_maxmultiplier = multiplier

    def update_score(self, circle, multiplier=1):
        self.stats_bubbles += 1
        self.update_max_multiplier(multiplier)
        self.bubbles -= 1
        points = multiplier * GameSettings.BUBBLE_MAXH//circle.height
        self.score +=  points
        self.stats_scoreround += points
        if DEBUG:
            print('updating score %d, round: %d circleh: %d mult: %d points: %d bubbles: %d' % (
                  self.score, self.stats_scoreround, circle.height, multiplier, points, self.bubbles)
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
