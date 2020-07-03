from bubblebuster.link import SpriteLink, LinkMan
import bubblebuster.sprite as sp
from bubblebuster.settings import GameSettings

import pygame
from enum import Enum

class BoxSpriteNames(Enum):
    BOX = 1
    EXPLOSION = 2
    CIRCLE = 3
    BOXGROUP = 4


class BoxSprite(SpriteLink):
    instance = None
    def __init__(self, name, width, height, x, y, color=(255, 255, 255, 25), fill_width=2):
        super().__init__()
        self.name = name
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        # dimensions
        self.width = width
        self.fill_width = fill_width
        self.height = height
        self.radius = self.height // 2 # for circles

        # position
        self.x = x
        self.y = y
        self.posx = x
        self.posy = y

        self.color = color

        # for carousel (should probably make a different class)
        self.parent = None
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(self.surface,
                         self.color,
                         self.rect,
                         self.fill_width
                         )
        self.surface.fill(self.color)
        self.rect = screen.blit(self.surface, (self.posx, self.posy))


class BoxSpriteMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        BoxSpriteMan.instance = self

    def compare(self, a, b):
        return a.name == b or a == b

    def add(self, sprite_name, width, height, x, y, duration=25, delta=1, color=(255, 255, 255), fill_width=2):
        if sprite_name == sp.BoxSpriteNames.BOX:
            sprite = sp.BoxSprite(sprite_name, width, height, x, y, color=color, fill_width=fill_width)
        elif sprite_name == sp.BoxSpriteNames.CIRCLE:
            sprite = sp.CircleSprite(sprite_name, width, height, x, y, color=color)
        elif sprite_name == sp.BoxSpriteNames.EXPLOSION:
            sprite = sp.ExplosionSprite(sprite_name, width, height, x, y, duration, delta, color=color)
        self.base_add(sprite)
        return sprite

    def add_sprite(self, sprite):
        self.base_add(sprite)
        return sprite

    def add_boxgroup(self, carousel):
        for rect in carousel.rects:
            self.base_add(rect)
        return carousel

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

