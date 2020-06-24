from link import Link, LinkMan, SpriteLink
from image import ImageMan, ImageNames
from collision import CollisionPairMan
from groups import GroupMan, GroupNames
import timer
from player import PlayerMan, PlayerNames
from font import Font, FontMan, FontNames
from settings import DEBUG

import pygame
from random import randint
from enum import Enum

class SpriteNames(Enum):
    EXPLODE = 1

class BoxSpriteNames(Enum):
    BOX = 1
    CIRCLEA = 2
    CIRCLEB = 3
    CIRCLEC = 4
    CIRCLED = 5
    CIRCLEE = 6
    CIRCLEF = 7
    CIRCLEG = 8
    CIRCLEH = 9
    CIRCLEI =10 
    CIRCLEJ = 11
    EXPLOSION = 12
    CIRCLE = 13

class LineSpriteNames(Enum):
    WALL_LEFT = 1
    WALL_RIGHT = 2
    WALL_TOP = 3
    WALL_BOTTOM = 4


class BoxSprite(SpriteLink):
    def __init__(self, name, width, height, x, y, color=(255, 255, 255)):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

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

        self.delta = 2

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen,
                                     self.color,
                                     self.rect,
                                     self.width
        )

    def move(self):
        width, height = pygame.display.get_surface().get_size()
        if self.posx >= width or self.posx <= 0:
            self.delta *= -1
        self.posx += self.delta

    def update(self):
        #self.move()
        pass



class LineSprite(SpriteLink):
    def __init__(self, name, start_xy, end_xy, color=(255, 255, 255), width=2):
        super().__init__()
        self.name = name
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
        circle.deltax *= -1
        circle.deltay *= -1
        # why do need to call this twice huh?
        circle.move()
        circle.update()


class CircleSprite(BoxSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltax = randint(-self.delta, self.delta)
        self.deltay = randint(-self.delta, self.delta)

    def move(self):
        self.posx += self.deltax
        self.posy += self.deltay

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, 
                                       self.color, 
                                       (self.posx, self.posy), 
                                       self.height//2,
                                       self.width)

    def update(self):
        self.move()

    def accept(self, circle):
        self.deltax *= -1
        self.deltay *= -1
        circle.deltax *= -1
        circle.deltay *= -1
        # resolve collisions for me please
        while pygame.sprite.collide_circle(self, circle):
            self.update()
            circle.update()

    def destroy_colliding_circles(self, multiplier):
        circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
        head = circle_group.nodeman.head
        while head:
            # there must be 
            # a better way
            if head.pSprite.name == BoxSpriteNames.CIRCLE and pygame.sprite.collide_circle(self, head.pSprite):

                multiplier += 1
                head.pSprite.color = (255, 0, 0)

                if DEBUG:
                    print('colliding circle destroyed, multiplier: %d' % multiplier)
                
                font_multiplier = FontMan.instance.find(FontNames.MULTIPLIER_TITLE)
                font_multiplier.text = multiplier

                command = timer.DestroySpriteCommand(head.pSprite, multiplier=multiplier)
                timer.TimerMan.instance.add(command, 100)

                head.pSprite.collision_enabled = False
            head = head.next

    def destroy(self, multiplier=1):
        #sprite = Sprite(SpriteNames.EXPLODE, ImageNames.EXPLODE, 50, 50, self.posx, self.posy)
        #SpriteMan.instance.add_sprite(sprite)
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        points = player.update_score(self, multiplier=multiplier)

        font_pointsvalue = FontMan.instance.add(Font(FontNames.MULTIPLIER, 'Comic Sans', 18, points, (255, 255, 255), (self.posx, self.posy)))
        timer.TimerMan.instance.add(timer.RemoveFontCommand(font_pointsvalue), 250)

        font_bubbles = FontMan.instance.find(FontNames.BUBBLES)
        font_bubbles.text = player.bubbles

        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score

        #timer.TimerMan.instance.add(timer.DestroySpriteCommand(sprite), 180)

        self.collision_enabled = False
        BoxSpriteMan.instance.remove(self)
        CollisionPairMan.instance.remove(self)
        group_manager = GroupMan.instance.find(GroupNames.CIRCLE)

        node = group_manager.find(self)
        if node: # what the
            group_manager.remove(node)
        self.destroy_colliding_circles(multiplier)


class ExplosionSprite(BoxSprite):
    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, 
                                       self.color, 
                                       (self.posx, self.posy), 
                                       self.height//2,
                                       self.width)

    def update(self):
        pass

    def accept(self, circle):
        if DEBUG:
            print('explosion collided with circle', circle)
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score
        circle.destroy(multiplier=1)


class BoxSpriteMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not BoxSpriteMan.instance:
            BoxSpriteMan.instance = BoxSpriteMan.__new__(BoxSpriteMan)
            BoxSpriteMan.instance.head = None
        return BoxSpriteMan.instance

    def compare(self, a, b):
        return a.name == b or a == b

    def add(self, sprite_name, width, height, x, y, color=(255, 255, 255)):
        if sprite_name == BoxSpriteNames.BOX:
            sprite = BoxSprite(sprite_name, width, height, x, y, color=color)
        elif sprite_name == BoxSpriteNames.CIRCLE:
            sprite = CircleSprite(sprite_name, width, height, x, y, color=color)
        elif sprite_name == BoxSpriteNames.EXPLOSION:
            sprite = ExplosionSprite(sprite_name, width, height, x, y, color=color)
        self.base_add(sprite)
        return sprite

    def add_sprite(self, sprite):
        self.base_add(sprite)
        return sprite

    def add_line_sprite(self, name, start_xy, end_xy, color=(255, 255, 255), width=2):
        sprite = LineSprite(name, start_xy, end_xy, color=color, width=width)
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
    instance = None

    @staticmethod
    def create():
        if not SpriteMan.instance:
            SpriteMan.instance = SpriteMan.__new__(SpriteMan)
            SpriteMan.instance.head = None
        return SpriteMan.instance

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


