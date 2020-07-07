from bubblebuster.timer import Command, TimeEventNames, TimerMan
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
import bubblebuster.collision as cl
import bubblebuster.sprite as sp


class ClickExplodeCommand(Command):
    def __init__(self, sprite):
        self.sprite = sprite
        self.name = TimeEventNames.CLICKEXPLODE

    def execute(self, delta_time):
        if self.sprite.duration:
            self.sprite.inc()
            TimerMan.instance.add(self, delta_time)
        else: # reset our explosion
            self.sprite.reset()
            # remove the sprite (could be recycled, but im lazy for now)
            sp.BoxSpriteMan.instance.remove(self.sprite)
            cl.CollisionPairMan.instance.remove(self.sprite)

