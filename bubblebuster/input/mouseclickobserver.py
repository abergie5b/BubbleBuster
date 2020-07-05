from bubblebuster.input import InputObserver
import bubblebuster.collision as collision
from bubblebuster.sound import SoundMan, SoundNames
import bubblebuster.scene.scenecontext as sc

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
        font.observer = self

    def reset(self, text):
        self.width, self.height = self.font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2,
                                 self.font.posy+self.height//2,
                                 self.width,
                                 self.height
                                 )

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if collision.intersect(self.rectA, self.rectB):
            bubblepop = SoundMan.instance.find(SoundNames.BUBBLEPOP)
            bubblepop.play()
            sc.SceneContext.instance.set_state(self.scene_change)

