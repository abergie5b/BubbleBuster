from bubblebuster.link import SpriteLink
import bubblebuster.sprite as sp

import pygame
from enum import Enum

class LineSpriteNames(Enum):
    WALL_LEFT = 1
    WALL_RIGHT = 2
    WALL_TOP = 3
    WALL_BOTTOM = 4
    NULL = 5


class LineSprite(SpriteLink):
    def __init__(self, name, start_xy, end_xy, color=(255, 255, 255), width=2):
        super().__init__()
        self.name = name
        self.type = sp.SpriteTypes.NULL
        self.start_xy = start_xy
        self.end_xy = end_xy
        self.color = color
        self.width = width
        self.rect = pygame.draw.line(pygame.Surface((0, 0)),
                                     self.color,
                                     self.start_xy,
                                     self.end_xy,
                                     self.width
                                     )

    def set_coords(self, startxy, endxy):
        self.start_xy = startxy
        self.end_xy = endxy

    def draw(self, screen):
        self.rect = pygame.draw.line(screen,
                                     self.color,
                                     self.start_xy,
                                     self.end_xy,
                                     self.width
                                     )

    def update(self):
        pass

    def accept(self, circle):
        # why do need to call this twice huh?
        circle.move()
        circle.update()
