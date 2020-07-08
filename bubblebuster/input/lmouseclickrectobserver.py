import bubblebuster.input as inp
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.font import FontMan, FontNames
import bubblebuster.scene.scene as sc
import bubblebuster.player as pl

import pygame

class LMouseClickRectObserver(inp.InputObserver):
    # this is just for weapon carousels for now
    def __init__(self, rect, weapon):
        self.rectA = rect
        self.weapon = weapon
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.observer = None

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if self.rectA.rect.colliderect(self.rectB):
            bubblepop = SoundMan.instance.find(SoundNames.BUBBLEPOP)
            bubblepop.play()

            if not self.rectA.selected:
                # click the rect, unclick others and remove observer
                self.rectA.parent.click(self.rectA)

                # equip the weapon
                player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
                player.weapon = self.weapon

                # update font
                fontplay = FontMan.instance.find(FontNames.PLAY)
                fontplay.text = 'Play!'
                fontplay.observer.reset(fontplay.text)

                # attach the observer for scene change
                self.observer = inp.InputMan.instance.lmouse.attach(
                                    inp.MouseClickObserver(fontplay, 
                                                           sc.SceneNames.SCENESWITCH
                                    )
                )
                self.rectA.observer = self.observer
            else:
                # clear 
                self.rectA.selected = False
                self.rectA.observer = None

                # clear font
                fontplay = FontMan.instance.find(FontNames.PLAY)
                fontplay.text = ''

                # if this doesnt work, maybe set the fontsize to 0?
                inp.InputMan.instance.lmouse.remove(self.observer)
