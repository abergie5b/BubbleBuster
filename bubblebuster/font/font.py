from bubblebuster.link import Link, LinkMan

import pygame
import pygame.freetype as pft
from enum import Enum

class FontNames(Enum):
    EXPLOSIONS = 1
    LIVES = 2
    SCORE = 3
    TIME = 4
    TITLE = 5
    NULL = 6
    MULTIPLIER = 7
    MULTIPLIER_TITLE = 8
    BUBBLES = 9
    PLAY = 10
    MENUTITLE = 11
    RULES = 12
    HIGHSCORES = 13
    EXIT = 14
    SETTINGS = 15
    BUBBLESMAXH = 16
    NUMBEROFEXPLOSIONS = 17
    EXPLOSIONDURATION = 18
    EXPLOSIONRADIUS = 19
    SMALLEXPLOSIONCOST = 20
    LARGEEXPLOSIONCOST = 21
    NUMBEROFBUBBLES = 22
    TOAST = 23
    BUBBLEPOPDELAY = 24
    LEVEL = 25
    STATS_MAXMULTIPLIER = 26
    STATS_BUBBLES = 27
    STATS_SCORE = 28
    STATS_EXPLOSIONSUSED = 29
    STATS_EXPLOSIONBONUS = 30
    STATS_ROUNDSCORE = 31
    SCOREROUND = 32
    STATS_EXPLOSIONSUSEDPREV = 33


class Font(Link):
    def __init__(self, font_name, font_style, font_size, text, color, posxy):
        super().__init__()
        self.font_name = font_name
        self.font_style = font_style
        self.font_size = font_size
        self.font = pygame.font.Font(font_style, font_size)
        self.text = text
        self.color = color
        self.posxy = posxy
        self.posx, self.posy = posxy

    def draw(self, screen):
        surface = self.font.render(str(self.text), True, self.color)
        screen.blit(surface, self.posxy)

    def update(self):
        pass


class FreeTypeFont(Link):
    def __init__(self, font_name, font_style, font_size, text, color, posxy):
        super().__init__()
        self.font_name = font_name
        self.font_style = font_style
        self.font_size = font_size
        self.font = pft.SysFont(font_style, font_size)
        self.text = text
        self.color = pygame.Color(*color)
        self.posxy = posxy
        self.posx, self.posy = posxy

    def draw(self, screen):
        surface, rect = self.font.render(str(self.text), self.color)
        screen.blit(surface, self.posxy)

    def update(self):
        pass


class FontMan(LinkMan):
    instance = None

    def compare(self, a, b):
        return a.font_name == b or a == b

    def add(self, font):
        self.base_add(font)
        return font

    def remove(self, font):
        self.base_remove(font)

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next

    def draw(self, screen):
        head = self.head
        while head:
            head.draw(screen)
            head = head.next

    def find(self, font):
        return self.base_find(font)

    @staticmethod
    def set_active(manager):
        FontMan.instance = manager