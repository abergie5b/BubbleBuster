from bubblebuster.timer import Command, TimeEventNames, TimerMan
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
import bubblebuster.collision as collision
import bubblebuster.sprite as sp


class ClickExplodeCommand(Command):
    def __init__(self, rect):
        self.rect = rect
        self.name = TimeEventNames.CLICKEXPLODE

    def execute(self, delta_time):
        if self.lives:
            self.rect.radius = self.radius + self.rect.delta
            self.rect.height = self.radius*2
            self.lives -= 1
            TimerMan.instance.add(self, delta_time)
        else: # reset our explosion
            self.rect.reset()
            #sp.BoxSpriteMan.instance.remove(self.rect)
            #collision.CollisionPairMan.instance.remove(self.rect)
            #node = self.circle_group.find(self.rect)
            #self.circle_group.remove(node)

