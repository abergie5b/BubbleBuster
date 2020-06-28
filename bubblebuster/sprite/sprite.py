from bubblebuster.link import Link, LinkMan
from bubblebuster.image import ImageMan
from bubblebuster.collision import CollisionPairMan

import pygame
from enum import Enum

class SpriteNames(Enum):
    EXPLODE = 1


class Sprite(Link):
    def __init__(self, name, image_name, width, height, x, y):
        super().__init__()
        self.name = name
        self.image = ImageMan.instance.find(image_name)
        self.rect = self.image.surface.get_rect()

        # dimensions
        self.width = width
        self.height = height

        # position
        self.posx = x
        self.posy = y

        # for collisions
        self.colx = x
        self.coly = y

        self.delta = 2

    @staticmethod
    def copy(sprite):
        return Sprite(sprite.name, sprite.image.name, sprite.width, sprite.height, sprite.posx, sprite.posy)

    def draw(self, screen):
        screen.blit(self.image.surface,
                    (self.posx, self.posy)
        )

    def update(self):
        pass

    def destroy(self):
        SpriteMan.instance.remove(self)
        CollisionPairMan.instance.remove(self)


class SpriteMan(LinkMan):

    def compare(self, a, b):
        return a.name == b

    def remove(self, sprite):
        self.base_remove(sprite)

    def add(self, sprite_name, image_name, width, height, x, y):
        sprite = Sprite(sprite_name, image_name, width, height, x, y)
        sprite.image.surface = pygame.transform.scale(sprite.image.surface, (width, height))
        self.base_add(sprite)
        return sprite

    def add_sprite(self, sprite):
        self.base_add(sprite)
        return sprite

    def draw(self, screen):
        head = self.head
        while head:
            head.draw(screen)
            head = head.next

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next
