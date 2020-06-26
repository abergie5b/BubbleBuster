from sprite import CircleSprite, BoxSpriteMan, BoxSpriteNames

from random import randint

import json


class CircleFactory:
    def __init__(self, group, manager):
        self.group = group
        self.manager = manager

    def generate_random(self, number_of_circles, max_xy=(800, 600), max_h=120):
            maxx, maxy = max_xy
            for x in range(number_of_circles):
                w, h = (1, randint(max_h//6, max_h))
                posxy = (randint(h//2, maxx-h-5), randint(h//2, maxy-h-5))
                self.create_circle(posxy, (w, h), self.get_random_color())

    def get_random_color(self):
        r = randint(75, 200)
        g = randint(75, 225)
        b = randint(75, 225)
        return (r, g, b)

    def create_circle(self, posxy, wh, color):
        x, y = posxy
        w, h = wh
        sprite = CircleSprite(BoxSpriteNames.CIRCLE, w, h, x, y, color=color)
        self.manager.add_sprite(sprite)
        self.group.add(sprite)
