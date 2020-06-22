from link import *
from image import *

import pygame
from enum import Enum

class SpriteNames(Enum):
    MOUSE1 = 1
    MOUSE2 = 2
    BOX = 3
    CIRCLE = 3

class BoxSprite(Link):
    def __init__(self, name, rect, width, height, x, y):
        super().__init__()
        self.name = name
        self.rect = rect

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

    def draw(self, screen):
        screen.blit(self.rect,
                    (self.posx, self.posy)
        )


class BoxSpriteMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not BoxSpriteMan.instance:
            BoxSpriteMan.instance = BoxSpriteMan.__new__(BoxSpriteMan)
            BoxSpriteMan.instance.head = None
        return BoxSpriteMan.instance

    def compare(self, a, b):
        return a.name == b

    def add(self, sprite_name, rect, width, height, x, y):
        sprite = BoxSprite(sprite_name, rect, width, height, x, y)
        #sprite.rect = pygame.transform.scale(sprite.rect, (width, height))
        self.base_add(sprite)

    def draw(self, screen):
        head = self.instance.head
        while head:
            head.draw(screen)
            head = head.next

    def update(self):
        head = self.instance.head
        while head:
            head.move()
            head = head.next


class Sprite(Link):
    def __init__(self, name, image_name, width, height, x, y):
        super().__init__()
        self.name = name
        self.image = ImageMan.instance.base_find(image_name)
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

    def draw(self, screen):
        screen.blit(self.image.surface,
                    (self.posx, self.posy)
        )

    def move(self):
        width, height = pygame.display.get_surface().get_size()
        if self.posx >= width or self.posx <= 0:
            self.delta *= -1
        self.posx += self.delta


class SpriteMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not SpriteMan.instance:
            SpriteMan.instance = SpriteMan.__new__(SpriteMan)
            SpriteMan.instance.head = None
        return SpriteMan.instance

    def compare(self, a, b):
        return a.name == b

    def add(self, sprite_name, image_name, width, height, x, y):
        sprite = Sprite(sprite_name, image_name, width, height, x, y)
        sprite.image.surface = pygame.transform.scale(sprite.image.surface, (width, height))
        self.base_add(sprite)

    def draw(self, screen):
        head = self.instance.head
        while head:
            head.draw(screen)
            head = head.next

    def update(self):
        head = self.instance.head
        while head:
            head.move()
            head = head.next

