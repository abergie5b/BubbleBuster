import bubblebuster.timer as timer
from bubblebuster.group import GroupMan, GroupNames

import pygame

class SecondChanceBubbleCommand(timer.Command):
    def __init__(self, sprite):
        self.sprite = sprite
        self.name = timer.TimeEventNames.SECONDCHANCE

    def execute(self, delta_time):
        self.sprite.image.fill((0, 0, 0), special_flags=pygame.BLEND_MULT)
        #timer.TimerMan.instance.add(
        #    timer.ColorChangeBubbleCommand(self.sprite, 25),
        #    1
        #)

