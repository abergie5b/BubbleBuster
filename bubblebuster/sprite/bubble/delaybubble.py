from bubblebuster.settings import GameSettings
from bubblebuster.settings import InterfaceSettings
from bubblebuster.font import Font, FontMan, FontNames
from bubblebuster.sprite.bubble import BubbleNames
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.sprite.circlesprite as csp

import pygame


class DelayBubble(csp.CircleSprite):
    def __init__(self, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(width, height, x, y, color=color, alpha=255)
        self.name = BubbleNames.DELAY
        self.type = sp.SpriteTypes.BUBBLE

    def proc(self):
        if self.proba_delaybubble:
            font_delaybubble = FontMan.instance.add(
                Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 18, "Delay!", InterfaceSettings.FONTCOLOR,
                     (self.posx+self.height//2, self.posy+self.height//2-25)) # above midpoint
            )
            timer.TimerMan.instance.add(timer.RemoveFontCommand(font_delaybubble), 1000)

            self.collision_enabled = False
            timer.TimerMan.instance.add(
                timer.ColorChangeBubbleCommand(self,
                                               self.image_red,
                                               GameSettings.BUBBLEPOPDELAY*2
                                               ),
                0
            )

            # do it
            command = timer.DestroySpriteCommand(self, explosion=sp.ExplosionSprite.instance)
            timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY*4)
            return True
        return False

