from bubblebuster.settings import GameSettings
from bubblebuster.settings import InterfaceSettings
from bubblebuster.font import Font, FontMan, FontNames
import bubblebuster.collision as cl
import bubblebuster.player as pl
import bubblebuster.group as group
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.sprite.circlesprite as csp
import bubblebuster.player as pl
import bubblebuster.level as le
import bubblebuster.sprite.bubble as bu

import pygame


class TwinBubble(csp.CircleSprite):
    def __init__(self, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(width, height, x, y, color=color, alpha=255)
        self.name = bu.BubbleNames.TWIN
        self.type = sp.SpriteTypes.BUBBLE

    def proc(self, explosion=None):
        if self.proba_multibubble:
            font_twinbubble = FontMan.instance.add(
                Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 18, "Twins!", InterfaceSettings.FONTCOLOR,
                     (self.posx+self.height//2, self.posy+self.height//2-25)) # above midpoint
            )
            timer.TimerMan.instance.add(timer.RemoveFontCommand(font_twinbubble), 1000)

            self.collision_enabled = False

            command = timer.DestroySpriteCommand(self, explosion=sp.ExplosionSprite.instance)
            timer.TimerMan.instance.add(command, 1)

            bubbletypea = bu.BubbleMan.instance.get_random()
            twina = bubbletypea.obj(self.width,
                    max(GameSettings.BUBBLE_MAXH//4, self.height//2),
                    self.rect.centerx,
                    self.rect.centery,
                    color=self.color)

            bubbletypeb = bu.BubbleMan.instance.get_random()
            twinb = bubbletypeb.obj(self.width,
                      max(GameSettings.BUBBLE_MAXH//4, self.height//2),
                      self.rect.centerx,
                      self.rect.centery,
                      color=self.color)

            # aod to sprite manager
            sp.BoxSpriteMan.instance.add_sprite(twinb)
            sp.BoxSpriteMan.instance.add_sprite(twina)

            # add to circle group, delay this
            timer.TimerMan.instance.add(timer.AddToCircleGroupCommand(twina), GameSettings.BUBBLEPOPDELAY)
            timer.TimerMan.instance.add(timer.AddToCircleGroupCommand(twinb), GameSettings.BUBBLEPOPDELAY)

            # attach to wall group
            wall_group = group.GroupMan.instance.find(group.GroupNames.WALL)
            cl.CollisionPairMan.instance.attach_to_group(wall_group, twina, cl.CollisionRectPair)
            cl.CollisionPairMan.instance.attach_to_group(wall_group, twinb, cl.CollisionRectPair)
            
            # adjust bubbles for level
            player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
            le.LevelMan.instance.current_level.target_bubbles += 2

            return True
        return False
