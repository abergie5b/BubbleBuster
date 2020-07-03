from bubblebuster.settings import GameSettings
from bubblebuster.image import ImageMan, ImageNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.settings import InterfaceSettings, DEBUG
from bubblebuster.font import Font, FontMan, FontNames
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.collision import CollisionPairMan
import bubblebuster.group as group
import bubblebuster.timer as timer
import bubblebuster.sprite as sp

import pygame
from random import randint


class CircleSprite(sp.BoxSprite):
    def __init__(self, name, image, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(name, width, height, x, y, color=color)

        # image
        self.image = pygame.transform.scale(image.surface, (self.height, self.height))
        red_bubble = ImageMan.instance.find(ImageNames.REDBUBBLE)
        self.image_red = pygame.transform.scale(red_bubble.surface, (self.height, self.height))

        # for movement
        self.delta = GameSettings.BUBBLE_MAXDELTA
        self.deltax = randint(-self.delta, self.delta)/100
        self.deltay = randint(-self.delta, self.delta)/100
        if not self.deltax:
            self.deltax = self.delta//100
        if not self.deltay:
            self.deltay = self.delta//100

        # for scoring
        self.hratio = self.height / GameSettings.BUBBLE_MAXH

    def move(self):
        self.posx += self.deltax
        self.posy += self.deltay

    def draw(self, screen):
        self.rect = screen.blit(self.image, (self.posx, self.posy))

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

    def destroy_colliding_circles(self, explosion):
        # explosion None ??
        circle_group = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        head = circle_group.nodeman.head
        while head:
            # there must be
            # a better way
            if head.pSprite.collision_enabled:
                if head.pSprite.name == sp.BoxSpriteNames.CIRCLE and pygame.sprite.collide_circle(self, head.pSprite):

                    explosion.multiplier += 1
                    # should do this better
                    head.pSprite.image = head.pSprite.image_red

                    if DEBUG:
                        print('colliding circle %s destroyed, multiplier: %d' % (head.pSprite, explosion.multiplier))

                    fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
                    timer.TimerMan.instance.remove(fadeout_command)

                    font_multiplier = FontMan.instance.find(FontNames.TOAST)
                    font_multiplier.text = str('Multiplier! %d' % explosion.multiplier)
                    font_multiplier.color = InterfaceSettings.FONTCOLOR

                    command = timer.DestroySpriteCommand(head.pSprite, explosion=explosion)
                    timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY)

                    sp.ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

                    head.pSprite.collision_enabled = False
            head = head.next

    def destroy(self, explosion):
        # what if explosion None huhh
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        points = player.update_score(self, multiplier=explosion.multiplier)

        # creatin new fonts .. bad
        font_pointsvalue = FontMan.instance.add(
            Font(FontNames.MULTIPLIER, InterfaceSettings.FONTSTYLE, 18, points, InterfaceSettings.FONTCOLOR,
                 (self.posx+self.height//2, self.posy+self.height//2)) # midpoint
        )
        timer.TimerMan.instance.add(timer.RemoveFontCommand(font_pointsvalue), 1000)

        font_bubbles = FontMan.instance.find(FontNames.BUBBLES)
        font_bubbles.text = player.level.bubbles

        # gotta do this somehwere else
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score

        font = FontMan.instance.find(FontNames.SCOREROUND)
        font.text = player.stats_scoreround

        self.play_sound()

        sp.BoxSpriteMan.instance.remove(self)
        CollisionPairMan.instance.remove(self)

        group_manager = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        node = group_manager.find(self)
        if node:  # what the
            group_manager.remove(node)

        self.destroy_colliding_circles(explosion)

        fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
        if explosion.multiplier > 1 and not fadeout_command:
            font_multiplier = FontMan.instance.find(FontNames.TOAST)
            timer.TimerMan.instance.add(timer.FadeOutFontCommand(font_multiplier, InterfaceSettings.FONTCOLOR), 1000)

