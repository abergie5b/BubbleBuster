from bubblebuster.input import InputObserver
from bubblebuster.collision import intersect
from bubblebuster.sound import SoundMan, SoundNames
import bubblebuster.scene as sp

import pygame

class MouseClickObserver(InputObserver):
    def __init__(self, font, scene_change, player=None):
        self.font = font
        self.width, self.height = font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2,
                                 self.font.posy+self.height//2,
                                 self.width,
                                 self.height
                                 )
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.scene_change = scene_change
        self.player = player

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            bubblepop = SoundMan.instance.find(SoundNames.BUBBLEPOP)
            bubblepop.play()
            sp.SceneContext.instance.set_state(self.scene_change, player=self.player)

