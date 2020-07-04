from bubblebuster.timer import Command, TimerMan, TimeEventNames
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.image import ImageMan, ImageNames

import pygame
from random import choice

class ColorChangeBubbleCommand(Command):
    def __init__(self, sprite, duration, end_on_grey=True):
        self.sprite = sprite
        self.duration = duration
        self.name = TimeEventNames.COLORCHANGEBUBBLE
        self.end_on_grey = end_on_grey

    def execute(self, delta_time):
        self.sprite.image = choice(self.sprite.images)
        if self.duration:
            TimerMan.instance.add(ColorChangeBubbleCommand(self.sprite, self.duration-1), 25)
        elif self.end_on_grey:
            self.sprite.image.fill((0, 0, 0), special_flags=pygame.BLEND_MULT)


