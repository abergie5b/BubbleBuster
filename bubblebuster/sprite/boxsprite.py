from bubblebuster.link import SpriteLink, LinkMan
import bubblebuster.sprite as sp

import pygame
from enum import Enum

class BoxSpriteNames(Enum):
    BOX = 1
    EXPLOSION = 2
    CIRCLE = 3


class BoxSprite(SpriteLink):
    instance = None
    def __init__(self, name, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__()
        self.name = name
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        # dimensions
        self.width = width
        self.height = height
        self.radius = self.height // 2 # for circles

        # position
        self.posx = x
        self.posy = y

        # for collisions
        self.colx = x
        self.coly = y

        self.color = color
        self.alpha = alpha

        self.delta = 2
        self.multiplier = 1

    def draw(self, screen):
        self.rect = pygame.draw.rect(self.surface,
                                     self.color,
                                     self.rect,
                                     self.width
                                     )
        screen.blit(self.surface, (self.posx, self.posy))


class BoxSpriteMan(LinkMan):
    instance = None

    def compare(self, a, b):
        return a.name == b or a == b

    def add(self, sprite_name, width, height, x, y, color=(255, 255, 255)):
        if sprite_name == sp.BoxSpriteNames.BOX:
            sprite = sp.BoxSprite(sprite_name, width, height, x, y, color=color)
        elif sprite_name == sp.BoxSpriteNames.CIRCLE:
            sprite = sp.CircleSprite(sprite_name, width, height, x, y, color=color)
        elif sprite_name == sp.BoxSpriteNames.EXPLOSION:
            sprite = sp.ExplosionSprite(sprite_name, width, height, x, y, color=color)
        self.base_add(sprite)
        return sprite

    def add_sprite(self, sprite):
        self.base_add(sprite)
        return sprite

    def add_line_sprite(self, name, start_xy, end_xy, color=(255, 255, 255), width=2):
        sprite = sp.LineSprite(name, start_xy, end_xy, color=color, width=width)
        self.base_add(sprite)
        return sprite

    def add_wall_sprite(self, name, start_xy, end_xy, color=(255, 255, 255), width=2):
        sprite = sp.WallSprite(name, start_xy, end_xy, color=color, width=width)
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

    def remove(self, sprite):
        self.base_remove(sprite)

    def find(self, sprite):
        return self.base_find(sprite)

    @staticmethod
    def set_active(manager):
        BoxSpriteMan.instance = manager

