from bubblebuster.timer import Command, TimeEventNames, TimerMan
from bubblebuster.group import GroupMan, GroupNames
from bubblebuster.settings import InterfaceSettings
import bubblebuster.collision as collision
import bubblebuster.sprite as sp


class ClickExplodeCommand(Command):
    def __init__(self, spritenode):
        self.spritenode = spritenode
        self.name = TimeEventNames.CLICKEXPLODE

    def execute(self, delta_time):
        if self.spritenode.pSprite.duration:
            self.spritenode.pSprite.inc()
            TimerMan.instance.add(self, delta_time)
        else: # reset our explosion
            self.spritenode.pSprite.reset()
            # i dont really want to do this
            # theres a better way to recycle
            sp.BoxSpriteMan.instance.remove(self.spritenode.pSprite)
            circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
            circle_group.remove(self.spritenode)

