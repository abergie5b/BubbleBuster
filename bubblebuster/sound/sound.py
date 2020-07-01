import pygame
from enum import Enum

from bubblebuster.link import *

class SoundNames(Enum):
    MUSICMENU = 1
    BUBBLEPOP = 2
    SMALLEXPLODE = 3
    LARGEEXPLODE = 4
    BUBBLE_MINIPOP = 5
    BUBBLE_SMALLPOP = 6
    BUBBLE_MEDIUMPOP = 7
    BUBBLE_LARGEPOP = 8


class Sound(Link):
    def __init__(self, name, filename):
        super().__init__()
        self.name = name
        self.filename = filename
        self.sound = pygame.mixer.Sound(filename)

    def play(self):
        self.sound.play()


class Music(Link):
    def __init__(self, name, filename):
        super().__init__()
        self.name = name
        self.filename = filename

    def play(self, loops=-1):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()


class SoundMan(LinkMan):
    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        sound = Sound(name, data)
        self.base_add(sound)

    def add_music(self, name, data):
        music = Music(name, data)
        self.base_add(music)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        SoundMan.instance = manager


