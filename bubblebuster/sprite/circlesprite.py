from bubblebuster.link import LinkMan
from bubblebuster.settings import GameSettings
from bubblebuster.image import ImageMan, ImageNames, BubbleImageMan
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.settings import InterfaceSettings, DEBUG
from bubblebuster.font import AlphaFont, FontMan, FontNames
from bubblebuster.sprite import BoxSpriteNames, BoxSpriteMan, BoxSprite, ExplosionSprite, SpriteTypes
import bubblebuster.collision as cl
import bubblebuster.group as group
import bubblebuster.timer as timer
import bubblebuster.player as pl
import bubblebuster.level as le

import pygame
from random import randint


class CircleSprite(BoxSprite):
    def __init__(self, width, height, x, y, color=(255, 255, 255), alpha=255):
        self.name = BoxSpriteNames.CIRCLE
        self.type = SpriteTypes.NULL
        super().__init__(BoxSpriteNames.CIRCLE, width, height, x, y, color=color)

        # red 
        red_bubble = ImageMan.instance.find(ImageNames.REDBUBBLE)
        self.original_image_red = self.image_red = pygame.transform.scale(red_bubble.surface, 
                                                                          (self.height, self.height)
        )

        # heres our bubble
        self.base_image = BubbleImageMan.instance.get_random()
        self.original_image = self.image = pygame.transform.scale(self.base_image.surface, 
                                                                  (self.height, self.height)
        )
        # make the bubble a little easier to see -o-
        self.image.fill((175, 175, 175), special_flags=pygame.BLEND_RGBA_MULT)

        # for movement
        self.delta = GameSettings.BUBBLE_MAXDELTA
        self.deltax = randint(-self.delta, self.delta)//100
        self.deltay = randint(-self.delta, self.delta)//100
        if not self.deltax:
            self.deltax = self.delta//100
        if not self.deltay:
            self.deltay = self.delta//100

        # for scoring
        self.hratio = self.height / GameSettings.BUBBLE_MAXH

        # gifts!
        self.proba_gift = GameSettings.BUBBLE_GIFTPROCPROBA <= randint(0, 100)/100

        # bubble procs
        self.proba_multibubble = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100
        self.proba_secondchance = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100
        self.proba_delaybubble = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100
        self.proba_spottedbubble = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100
        self.proba_nukebubble = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100
        self.proba_slipperybubble = GameSettings.BUBBLE_PROCPROBA >= randint(0, 100)/100

        # state
        self.bubble_collision_disabled = False
        # has collided with another circle 
        self.has_collided = False

    def move(self):
        self.posx += self.deltax
        self.posy += self.deltay

    def draw(self, screen):
        self.rect = screen.blit(self.image,
                                (self.posx, self.posy)
        )

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

    def proc(self):
        raise NotImplementedError('proc not implemented for circle sprite base class')

    def prepare_explode(self, explosion=None):
        self.image = self.image_red
        self.collision_enabled = False
        self.has_collided = True

        # this IncreaseBubbleRadiusCommand.duration is quite random
        # since the timerman is based on time not frames ideally we could have
        # something that runs more consistently
        command = timer.IncreaseBubbleRadiusCommand(self, GameSettings.BUBBLEPOPDELAY//25)
        timer.TimerMan.instance.add(command, 0)

        # stop the bubble
        command = timer.SetBubbleDeltaCommand(self, 0, 0)
        timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY-GameSettings.BUBBLEPOPDELAY//4)

        # destroy
        command = timer.DestroySpriteCommand(self, explosion=explosion)
        timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY)

    def destroy_colliding_circles(self, explosion):
        circle_group = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        head = circle_group.nodeman.head
        while head:
            if head.pSprite.collision_enabled:
                # this is not pretty
                if head.pSprite.type == SpriteTypes.BUBBLE \
                   and not head.pSprite.bubble_collision_disabled \
                   and pygame.sprite.collide_circle(self, head.pSprite):

                    # stats
                    explosion.multiplier += 1
                    ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

                    if DEBUG:
                        print('colliding circle %s destroyed, multiplier: %d' % (head.pSprite, explosion.multiplier))

                    # multiplier font text
                    fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
                    timer.TimerMan.instance.remove(fadeout_command)

                    font_multiplier = FontMan.instance.find(FontNames.TOAST)
                    font_multiplier.text = str('Multiplier! %d' % explosion.multiplier)
                    font_multiplier.color = InterfaceSettings.FONTCOLOR

                    # do the thing
                    procd = head.pSprite.proc()
                    if not procd: # destroy
                        head.pSprite.prepare_explode()

            head = head.next

    def proc(self):
        raise NotImplementedError('procs are not implemented for base class circle sprites')

    def destroy(self, explosion):
        '''
        destroy this bubble and check for neighboring collisions
        bubble might even get a second chance at life, who knows
        '''
        if not explosion:
            explosion = ExplosionSprite.instance

        ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

        # scoreboard
        player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        points = player.update_score(self, multiplier=explosion.multiplier)

        # font score
        player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score

        # show score bubble text
        font_pointsvalue = FontMan.instance.add(
            AlphaFont(FontNames.MULTIPLIER, InterfaceSettings.FONTSTYLE, 18, points, InterfaceSettings.FONTCOLOR,
                 (self.posx+self.height//2, self.posy+self.height//2)) # midpoint
        )
        timer.TimerMan.instance.add(timer.RemoveFontCommand(font_pointsvalue), 500)

        # bubble texts
        target_bubbles = le.LevelMan.instance.current_level.target_bubbles
        if target_bubbles >= 0:
            font_bubbles = FontMan.instance.find(FontNames.BUBBLES)
            font_bubbles.text = target_bubbles
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score
        font = FontMan.instance.find(FontNames.SCOREROUND)
        font.text = player.stats_scoreround

        # sound
        self.play_sound()

        # quietly remove myself
        BoxSpriteMan.instance.remove(self)
        cl.CollisionPairMan.instance.remove(self)

        group_manager = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        node = group_manager.find(self)
        if node:  # what the
            group_manager.remove(node)

        # collisions
        self.destroy_colliding_circles(explosion)

        # fade the toast
        fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
        if explosion.multiplier > 1 and not fadeout_command:
            font_multiplier = FontMan.instance.find(FontNames.TOAST)
            timer.TimerMan.instance.add(timer.FadeOutFontCommand(font_multiplier, InterfaceSettings.FONTCOLOR), 1000)

    def accept(self, circle):
        assert isinstance(circle, CircleSprite)

        if DEBUG:
            print('%s bubble collided with %s bubble' % (self, circle))

        procd = circle.proc()
        if not procd: # destroy me
            circle.prepare_explode()


class CircleSpriteMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        CircleSpriteMan.instance = self

    def compare(self, a, b):
        return a.name == b or a == b

    def add(self, sprite_name, width, height, x, y, color=(255, 255, 255)):
        sprite = CircleSprite(sprite_name, width, height, x, y, color=color)
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

    def remove(self, sprite):
        self.base_remove(sprite)

    def find(self, sprite):
        return self.base_find(sprite)

    @staticmethod
    def set_active(manager):
        CircleSpriteMan.instance = manager

