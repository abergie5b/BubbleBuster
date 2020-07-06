import bubblebuster.collision as collision
from bubblebuster.input import MouseClickObserver
import bubblebuster.scene.scenecontext as sccxt

class MouseClickExitObserver(MouseClickObserver):
    def __init__(self, font, scene):
        super().__init__(font, scene)

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if collision.intersect(self.rectA, self.rectB):
            # handle this somewhere else please
            sccxt.SceneContext.instance.game.running = False

