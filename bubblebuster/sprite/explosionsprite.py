import bubblebuster.sprite as sp
from bubblebuster.settings import DEBUG
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import FontMan, FontNames
import bubblebuster.timer as timer

import pygame

class ExplosionSprite(sp.BoxSprite):
    instance = None
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
