from bubblebuster.settings import GameSettings
from bubblebuster.image import ImageMan, ImageNames, BubbleImageMan
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.settings import InterfaceSettings, DEBUG
from bubblebuster.font import AlphaFont, Font, FontMan, FontNames
from bubblebuster.sprite.bubble import BubbleNames
import bubblebuster.collision as cl
import bubblebuster.player as pl
import bubblebuster.group as group
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.sprite.circlesprite as csp

import pygame
from random import randint, choice


class IronBubble(csp.CircleSprite):
    def __init__(self, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(width, height, x, y, color=color, alpha=255)
        self.name = BubbleNames.IRON
        self.type = sp.SpriteTypes.BUBBLE

