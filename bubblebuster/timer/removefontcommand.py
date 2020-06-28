from bubblebuster.timer import Command, TimeEventNames
from bubblebuster.font import FontMan

class RemoveFontCommand(Command):
    def __init__(self, font):
        self.font = font
        self.name = TimeEventNames.REMOVEFONT

    def execute(self, delta_time):
        FontMan.instance.remove(self.font)


