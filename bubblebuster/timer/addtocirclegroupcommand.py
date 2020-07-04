from bubblebuster.timer import Command, TimeEventNames
from bubblebuster.group import GroupMan, GroupNames

import pygame
from random import choice

class AddToCircleGroupCommand(Command):
    def __init__(self, sprite):
        self.sprite = sprite
        self.name = TimeEventNames.ADDTOCIRCLEGROUP

    def execute(self, delta_time):
        circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
        circle_group.add(self.sprite)

