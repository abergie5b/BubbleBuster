from bubblebuster.input import InputObserver
from bubblebuster.collision import intersect
from bubblebuster.settings import GameSettings
from bubblebuster.font import FontMan

import pygame

class MouseClickSettingsObserver(InputObserver):
    def __init__(self, font, setting, font_name, increment):
        self.font = font
        self.width, self.height = font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2,
                                 self.font.posy+self.height//2,
                                 self.width,
                                 self.height
                                 )
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.setting = setting
        self.font_name = font_name
        self.increment = increment

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            value = getattr(GameSettings, self.setting)
            if value + self.increment >= 0: # nice try
                setattr(GameSettings, self.setting, value + self.increment)
                # not ideal to do like this
                value = getattr(GameSettings, self.setting)
                font = FontMan.instance.find(self.font_name)
                font.text = str(value)
