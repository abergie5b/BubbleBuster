from bubblebuster.input import MouseClickObserver
import bubblebuster.collision as collision
from bubblebuster.settings import InterfaceSettings

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

