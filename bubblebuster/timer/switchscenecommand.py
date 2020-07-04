from bubblebuster.timer import Command, TimeEventNames
import bubblebuster.scene.scenecontext as sc
import bubblebuster.input as input

class SwitchSceneCommand(Command):
    def __init__(self, destination, player=None, onkeypress=None):
        self.name = TimeEventNames.SWITCHSCENE
        self.destination = destination
        self.player = player
        self.onkeypress = onkeypress

    def execute(self, delta_time):
        if self.onkeypress:
            self.onkeypress = False
            input.InputMan.instance.lmouse.attach(input.KeyPressObserver(self, delta_time))
            input.InputMan.instance.rmouse.attach(input.KeyPressObserver(self, delta_time))
            input.InputMan.instance.keypress.attach(input.KeyPressObserver(self, delta_time))
        else:
            sc.SceneContext.instance.set_state(self.destination, player=self.player)

