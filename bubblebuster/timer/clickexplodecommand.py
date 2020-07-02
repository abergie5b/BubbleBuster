from bubblebuster.timer import Command, TimeEventNames, TimerMan
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
import bubblebuster.collision as collision
import bubblebuster.sprite as sp


class ClickExplodeCommand(Command):
    def __init__(self, x, y, radius, radius_delta, lives):
        self.x = x
        self.y = y
        self.width = 2
        self.radius = radius
        self.delta = radius_delta
        self.original_lives = lives
        self.lives = lives
        self.color = InterfaceSettings.EXPLOSIONCOLOR
        self.rect = None
        self.circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
        self.name = TimeEventNames.CLICKEXPLODE

    def execute(self, delta_time):
        if self.lives == self.original_lives:
            self.rect = sp.BoxSpriteMan.instance.add(sp.BoxSpriteNames.EXPLOSION,
                                                     self.width,
                                                     self.radius*2,
                                                     self.x,
                                                     self.y,
                                                     color=self.color
                                                     )
            self.circle_group.add(self.rect)

        self.rect.radius = self.radius = self.radius + self.delta
        self.rect.height = self.radius*2
        self.lives -= 1

        if self.lives:
            TimerMan.instance.add(self, delta_time)
        else:
            sp.BoxSpriteMan.instance.remove(self.rect)
            collision.CollisionPairMan.instance.remove(self.rect)
            node = self.circle_group.find(self.rect)
            self.circle_group.remove(node)

