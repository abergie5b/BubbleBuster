from bubblebuster.timer import TimerMan, Command, TimeEventNames

import pygame

class IncreaseBubbleRadiusCommand(Command):
    def __init__(self, sprite, duration):
        self.sprite = sprite
        self.name = TimeEventNames.INCREASEBUBBLERADIUS
        self.duration = duration

    def execute(self, delta_time):
        if self.duration:
            self.sprite.height += 2
            self.sprite.radius = self.sprite.height // 2
            self.sprite.image = pygame.transform.scale(self.sprite.original_image_red,
                                                       (self.sprite.height, self.sprite.height)
            )
            # keep center
            self.sprite.posx -= 1
            self.sprite.posy -= 1
            self.duration -= 1
            TimerMan.instance.add(self, 1)

