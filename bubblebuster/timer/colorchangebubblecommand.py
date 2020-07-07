from bubblebuster.timer import Command, TimerMan, TimeEventNames
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.image import ImageMan, ImageNames

import pygame
from random import choice


class ColorChangeBubbleCommand(Command):
    def __init__(self, sprite, image, duration, freq=1):
        self.sprite = sprite
        self.image = image
        self.duration = duration
        self.freq = freq
        self.name = TimeEventNames.COLORCHANGEBUBBLE
        self.flip = True

    def execute(self, delta_time):
        if self.duration:
            self.sprite.image = self.image if self.flip else self.sprite.original_image
            self.flip ^= 0x1
            self.duration -= 1
            TimerMan.instance.add(self, self.freq)

