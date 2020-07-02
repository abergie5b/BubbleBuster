from bubblebuster.input import MouseClickObserver, InputObserver
import bubblebuster.collision as collision
from bubblebuster.settings import InterfaceSettings

import pygame

class MouseHoverHighlightObserver(MouseClickObserver):
    def __init__(self, font, scene):
        super().__init__(font, scene)

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if collision.intersect(self.rectA, self.rectB):
            self.font.color = InterfaceSettings.MOUSEHIGHLIGHTFONTCOLOR
        else:
            self.font.color = InterfaceSettings.FONTCOLOR


class MouseHoverHighlightRectObserver(InputObserver):
    def __init__(self, rect):
        self.rectA = rect
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.rectA_color = self.rectA.color

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if self.rectA.rect.colliderect(self.rectB): # click
            self.rectA.color = (205, 205, 205, 50)
        elif not self.rectA.selected:
            self.rectA.color = self.rectA_color

