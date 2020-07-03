import bubblebuster.sprite as sp
from bubblebuster.settings import DEBUG
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import FontMan, FontNames
import bubblebuster.timer as timer

import pygame

class ExplosionSprite(sp.BoxSprite):
    instance = None
    def __init__(self, name, width, height, x, y, duration, radius_delta, color=(255, 255, 255), alpha=255):
        super().__init__(name, width, height, x, y, color=color)
        # note: no image for this yet

        # for scoring
        self.multiplier = 1

        # for weapons
        self.duration = duration
        self.originald = duration
        self.radius_delta = radius_delta
        self.originalr = height
        self.originalx = x
        self.originaly = y

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen,
                                       self.color,
                                       (self.posx, self.posy),
                                       self.height//2,
                                       self.width)

    def update(self):
        pass

    def accept(self, circle):
        ExplosionSprite.instance = self
        ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time
        if DEBUG:
            print('explosion collided with circle', circle)
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score
        circle.destroy(explosion=self)

    def inc(self):
        if DEBUG and self.duration % 5 == 0:
            print('firing explosion at (%d, %d) duration %d height %d width %d' % (
                  self.posx, self.posy, self.duration, self.height, self.width
            ))
        self.radius += self.radius_delta
        self.height = self.radius*2
        self.duration -= 1

    def reset(self):
        if DEBUG:
            print('resetting explosion at (%d, %d) duration %d height %d width %d' % (
                  self.posx, self.posy, self.duration, self.height, self.width
            ))
        self.radius = self.originalr
        self.height = self.radius*2
        self.posx = self.originalx
        self.posy = self.originaly
        self.duration = self.originald
