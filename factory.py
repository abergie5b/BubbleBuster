from sprite import CircleSprite, BoxSpriteMan, BoxSpriteNames

from random import randint


class CircleFactory:
    def __init__(self, group):
        self.group = group

    def generate_random(self, number_of_circles, max_xy=(800, 600), max_h=120):
            maxx, maxy = max_xy
            for x in range(number_of_circles):
                posxy = (randint(max_h, maxx), randint(max_h, maxy))
                wh = (1, randint(max_h//2, max_h))
                self.create_circle(posxy, wh, self.get_random_color())

    def get_random_color(self):
        r = randint(0, 150)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

    def create_circle(self, posxy, wh, color):
        x, y = posxy
        w, h = wh
        sprite = CircleSprite(BoxSpriteNames.CIRCLE, w, h, x, y, color=color)
        BoxSpriteMan.instance.add_sprite(sprite)
        self.group.add(sprite)
