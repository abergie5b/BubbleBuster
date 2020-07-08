from bubblebuster.timer import Command, TimeEventNames

class SetBubbleDeltaCommand(Command):
    def __init__(self, sprite, deltax, deltay):
        self.sprite = sprite
        self.deltax = deltax
        self.deltay = deltay
        self.name = TimeEventNames.SETBUBBLEDELTA

    def execute(self, delta_time):
        self.sprite.deltax = self.deltax
        self.sprite.deltay = self.deltay

