from bubblebuster.timer import Command, TimeEventNames
import bubblebuster.input as input
import bubblebuster.scene.scene as sc

class SwitchSceneCommand(Command):
    def __init__(self, destination, player=None, onkeypress=False):
        self.name = TimeEventNames.SWITCHSCENE
        self.destination = destination # SceneNames
        self.player = player
        self.onkeypress = onkeypress

    def execute(self, delta_time):
        if self.onkeypress:
            self.onkeypress = False
            input.InputMan.instance.lmouse.attach(input.KeyPressObserver(self, delta_time))
            input.InputMan.instance.rmouse.attach(input.KeyPressObserver(self, delta_time))
            input.InputMan.instance.keypress.attach(input.KeyPressObserver(self, delta_time))
        else:
            sc.SceneMan.instance.set_scene(self.destination)

