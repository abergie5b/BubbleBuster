from bubblebuster.settings import DEBUG
import bubblebuster.collision as cl
import bubblebuster.timer as timer
import bubblebuster.sprite as sp
import bubblebuster.group as gp


import pygame

class ExplosionSprite(sp.BoxSprite):
    instance = None
    def __init__(self, name, width, height, x, y, duration, radius_delta, color=(255, 255, 255)):
        super().__init__(name, width, height, x, y, color=color)
        # note: no image for this yet

        # type
        self.type = sp.SpriteTypes.EXPLOSION

        # for scoring
        self.multiplier = 1

        # for weapons
        self.duration = duration
        self.originald = duration
        self.radius_delta = radius_delta
        self.originalr = height
        self.originalx = x
        self.originaly = y

        # back pointer
        self.weapon = None

        # state
        self.has_collided = False # always

    def draw(self, screen):
        # get the radius 
        radius = self.height // 2

        # fix for simulation when timerman does not run in the loop
        # (width greater than radius exception)
        while radius < self.width:
            radius += 1

        self.rect = pygame.draw.circle(screen,
                                       self.color,
                                       (self.posx, self.posy),
                                       radius,
                                       self.width)

    def update(self):
        pass

    def accept(self, circle):
        ExplosionSprite.instance = self
        ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

        if DEBUG:
            print('explosion collided with circle', circle)

        procd = circle.proc()
        if not procd: # destroy me
            circle.prepare_explode(explosion=self)

            # this bubble can collide with others now
            #circle_group = gp.GroupMan.instance.find(gp.GroupNames.CIRCLE)
            #cl.CollisionPairMan.instance.attach_to_group(circle_group, circle, cl.CollisionCirclePair)

            #circle.destroy(explosion=self)

        # when explosion collides with circle, destroy the explosion
        command = timer.TimerMan.instance.find(timer.TimeEventNames.CLICKEXPLODE)
        timer.TimerMan.instance.remove(command)

        # reset the explosion for next time
        self.reset()

        # remove it from groups after collision with a bubble
        sp.BoxSpriteMan.instance.remove(self)
        cl.CollisionPairMan.instance.remove(self)

    def inc(self):
        if DEBUG and self.duration % 5 == 0:
            print('firing explosion at (%d, %d) duration %d height %d width %d' % (
                  self.posx, self.posy, self.duration, self.height, self.width
            ))
        self.radius += self.radius_delta
        self.height = self.radius*2
        self.duration -= 1

    def reset(self):
        if DEBUG:
            print('resetting explosion at (%d, %d) duration %d height %d width %d' % (
                  self.posx, self.posy, self.duration, self.height, self.width
            ))
        self.radius = self.originalr
        self.height = self.radius*2
        self.posx = self.originalx
        self.posy = self.originaly
        self.duration = self.originald
        self.weapon.is_active = False

