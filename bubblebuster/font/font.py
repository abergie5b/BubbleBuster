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
    CURRENTLEVEL = 34
    STATS_EXPLOSIONBONUSA = 35
    STATS_EXPLOSIONBONUSB = 36
    STATS_EXPLOSIONBONUSC = 37
    STATS_EXPLOSIONBONUSD = 38
    SCENESWITCH_PRESSANYKEY = 39
    LEVELTYPE = 40
    LEVELDESCRIPTION = 41
    LEVELHINT = 42
    SCENESWITCHHINT = 43
    SCOREROUNDLABEL = 44
    SCORELABEL = 45
    EXPLOSIONSLABEL = 46
    TIMELABEL = 47
    BUBBLESLABEL = 48

    

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
        self.surface = self.font.render(str(self.text), True, self.color)
        self.is_draw_enabled = True

    def draw(self, screen):
        self.surface = self.font.render(str(self.text), True, self.color)
        screen.blit(self.surface, self.posxy)

    def update(self):
        pass


class AlphaFont(Link):
    def __init__(self, font_name, font_style, font_size, text, color, posxy, alpha=100):
        super().__init__()
        self.font_name = font_name
        self.font_style = font_style
        self.font_size = font_size
        self.font = pygame.font.Font(font_style, font_size)
        self.text = text
        self.color = color
        self.posxy = posxy
        self.posx, self.posy = posxy
        self.surface = self.font.render(str(self.text), True, self.color)
        self.alpha = (0, 0, 0, alpha)
        self.alpha_surf = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        self.alpha_surf.fill(self.alpha)
        self.surface.blit(self.alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.is_draw_enabled = True

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(str(self.text), True, self.color)
        self.alpha_surf = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)

    def draw(self, screen):
        #self.surface.blit(self.alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.surface, self.posxy)

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
    def __init__(self):
        super().__init__()
        FontMan.instance = self

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
            if head.is_draw_enabled:
                head.draw(screen)
            head = head.next

    def find(self, font):
        return self.base_find(font)

    @staticmethod
    def set_active(manager):
        FontMan.instance = manager
