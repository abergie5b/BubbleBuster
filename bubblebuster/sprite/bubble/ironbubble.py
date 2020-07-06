from bubblebuster.settings import InterfaceSettings
from bubblebuster.font import Font, FontMan, FontNames
from bubblebuster.sprite.bubble import BubbleNames
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.sprite.circlesprite as csp

import pygame


class IronBubble(csp.CircleSprite):
    def __init__(self, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(width, height, x, y, color=color, alpha=255)
        self.name = BubbleNames.IRON
        self.type = sp.SpriteTypes.BUBBLE

    def proc(self):
        if self.proba_secondchance:
            font_secondchance = FontMan.instance.add(
                Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 18, "Iron Bubble!", InterfaceSettings.FONTCOLOR,
                     (self.posx+self.height//2, self.posy+self.height//2-25)) # above midpoint
            )
            timer.TimerMan.instance.add(timer.RemoveFontCommand(font_secondchance), 1000)


            self.proba_secondchance = 0 # no more second chances for you mate
            self.bubble_collision_disabled = True

            command = timer.SecondChanceBubbleCommand(self)
            timer.TimerMan.instance.add(command, 1)
            return True
        return False
