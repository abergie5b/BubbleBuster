from bubblebuster.timer import Command, TimeEventNames
import bubblebuster.level as le
import bubblebuster.settings as st

class SetGameOverCommand(Command):
    def __init__(self):
        self.name = TimeEventNames.SETGAMEOVER

    def execute(self, delta_time):
        le.LevelMan.instance.current_level.defeat = True

