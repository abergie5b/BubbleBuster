import bubblebuster.input as inp
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.font import FontMan, FontNames
import bubblebuster.scene as sc

import pygame

class LMouseClickRectObserver(inp.InputObserver):
    # this is just for weapon carousels for now
    def __init__(self, rect, player, weapon):
        self.rectA = rect
        self.player = player
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
                self.rectA.parent.click(self.rectA)
                self.player.weapon = self.weapon

                fontplay = FontMan.instance.find(FontNames.PLAY)
                fontplay.text = 'Play!'
                fontplay.observer.reset(fontplay.text)

                self.observer = inp.InputMan.instance.lmouse.attach(inp.MouseClickObserver(fontplay, sc.SceneNames.SCENESWITCH, player=self.player))
            else:
                self.rectA.selected = False
                fontplay = FontMan.instance.find(FontNames.PLAY)
                fontplay.text = ''
                # if this doesnt work, maybe set the fontsize to 0?
                inp.InputMan.instance.lmouse.remove(self.observer)

