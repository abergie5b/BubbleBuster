from bubblebuster.timer import Command, TimeEventNames

class DestroySpriteCommand(Command):
    def __init__(self, sprite, explosion=None):
        self.sprite = sprite
        self.explosion = explosion
        self.name = TimeEventNames.DESTROYSPRITE

    def execute(self, delta_time):
        self.sprite.destroy(explosion=self.explosion)

