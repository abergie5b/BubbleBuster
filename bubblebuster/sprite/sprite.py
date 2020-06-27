from bubblebuster.link import Link, LinkMan, SpriteLink
from bubblebuster.image import ImageMan, ImageNames
from bubblebuster.collision import CollisionPairMan
import bubblebuster.group as group
import bubblebuster.timer as timer
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import Font, FontMan, FontNames
from bubblebuster.settings import DEBUG, InterfaceSettings, GameSettings
from bubblebuster.sound import SoundMan, SoundNames

import pygame
from random import randint
from enum import Enum

class SpriteNames(Enum):
    EXPLODE = 1

class BoxSpriteNames(Enum):
    BOX = 1
    EXPLOSION = 2
    CIRCLE = 3

class LineSpriteNames(Enum):
    WALL_LEFT = 1
    WALL_RIGHT = 2
    WALL_TOP = 3
    WALL_BOTTOM = 4


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
        if self.name == LineSpriteNames.WALL_LEFT or self.name == LineSpriteNames.WALL_RIGHT:
            circle.deltax *= -1
        else:
            circle.deltay *= -1

        # why do need to call this twice huh?
        circle.move()
        circle.update()


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


class CircleSprite(BoxSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltax = randint(-self.delta, self.delta)
        self.deltay = randint(-self.delta, self.delta)
        self.hratio = self.height / GameSettings.BUBBLE_MAXH
        #self.image = pygame.image.load('resources/bubble_transparent.png').convert_alpha()
        #self.surface = self.image.subsurface(pygame.Rect(54, 50, 238, 238))

    def move(self):
        self.posx += self.deltax
        self.posy += self.deltay

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen,
                                       self.color, 
                                       (self.posx, self.posy), 
                                       self.height//2,
                                       self.width)

        #screen.blit(self.surface, (self.posx, self.posy))
        #screen.blit(self.image, (self.posx, self.posy))
        #self.rect = screen.blit(self.surface, (self.posx, self.posy))

    def update(self):
        self.move()

    def play_sound(self):
        if self.hratio >= 0.75:
            sound = SoundMan.instance.find(SoundNames.BUBBLE_LARGEPOP)
        elif self.hratio >= 0.5:
            sound = SoundMan.instance.find(SoundNames.BUBBLE_MEDIUMPOP)
        elif self.hratio >= 0.25:
            sound = SoundMan.instance.find(SoundNames.BUBBLE_SMALLPOP)
        else:
            sound = SoundMan.instance.find(SoundNames.BUBBLE_MINIPOP)
        sound.play()

    def accept(self, circle):
        self.deltax *= -1
        self.deltay *= -1
        circle.deltax *= -1
        circle.deltay *= -1
        # resolve collisions for me please! please!
        while pygame.sprite.collide_circle(self, circle):
            self.update()
            circle.update()

    def destroy_colliding_circles(self, explosion):
        # explosion None ??
        circle_group = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        head = circle_group.nodeman.head
        while head:
            # there must be 
            # a better way
            if head.pSprite.collision_enabled:
                if head.pSprite.name == BoxSpriteNames.CIRCLE and pygame.sprite.collide_circle(self, head.pSprite):

                    explosion.multiplier += 1
                    head.pSprite.color = (255, 0, 0)

                    if DEBUG:
                        print('colliding circle %s destroyed, multiplier: %d' % (head.pSprite, explosion.multiplier))
                    
                    fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
                    timer.TimerMan.instance.remove(fadeout_command)

                    font_multiplier = FontMan.instance.find(FontNames.TOAST)
                    font_multiplier.text = str('Multiplier! %d' % explosion.multiplier)
                    font_multiplier.color = InterfaceSettings.FONTCOLOR

                    command = timer.DestroySpriteCommand(head.pSprite, explosion=explosion)
                    timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY)

                    ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

                    head.pSprite.collision_enabled = False
            head = head.next

    def destroy(self, explosion):
        # what if explosion None huhh
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        points = player.update_score(self, multiplier=explosion.multiplier)

        font_pointsvalue = FontMan.instance.add(Font(FontNames.MULTIPLIER, InterfaceSettings.FONTSTYLE, 18, points, (255, 255, 255), (self.posx, self.posy)))
        timer.TimerMan.instance.add(timer.RemoveFontCommand(font_pointsvalue), 1000)

        font_bubbles = FontMan.instance.find(FontNames.BUBBLES)
        font_bubbles.text = player.bubbles

        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score

        font = FontMan.instance.find(FontNames.SCOREROUND)
        font.text = player.stats_scoreround

        self.play_sound()

        BoxSpriteMan.instance.remove(self)
        CollisionPairMan.instance.remove(self)

        group_manager = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        node = group_manager.find(self)
        if node: # what the
            group_manager.remove(node)

        self.destroy_colliding_circles(explosion)

        fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
        if explosion.multiplier > 1 and not fadeout_command:
            font_multiplier = FontMan.instance.find(FontNames.TOAST)
            timer.TimerMan.instance.add(timer.FadeOutFontCommand(font_multiplier, InterfaceSettings.FONTCOLOR), 1000)


class ExplosionSprite(BoxSprite):
    instance = None
    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, 
                                       self.color, 
                                       (self.posx, self.posy), 
                                       self.height//2,
                                       self.width)

    def update(self):
        pass

    def accept(self, circle):
        ExplosionSprite.instance = self
        ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time
        if DEBUG:
            print('explosion collided with circle', circle)
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score
        circle.destroy(explosion=self)


class BoxSpriteMan(LinkMan):
    instance = None

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

    @staticmethod
    def set_active(manager):
        BoxSpriteMan.instance = manager


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

