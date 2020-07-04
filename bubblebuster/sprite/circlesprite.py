from bubblebuster.settings import GameSettings
from bubblebuster.image import ImageMan, ImageNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.settings import InterfaceSettings, DEBUG
from bubblebuster.font import Font, FontMan, FontNames
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.collision import CollisionPairMan, CollisionRectPair
from bubblebuster.sprite import BoxSpriteNames, BoxSpriteMan
import bubblebuster.group as group
import bubblebuster.timer as timer
import bubblebuster.sprite as sp

import pygame
from random import randint, choice


class CircleSprite(sp.BoxSprite):
    def __init__(self, name, width, height, x, y, color=(255, 255, 255), alpha=255):
        super().__init__(name, width, height, x, y, color=color)

        # red 
        red_bubble = ImageMan.instance.find(ImageNames.REDBUBBLE)
        self.image_red = pygame.transform.scale(red_bubble.surface, (self.height, self.height))

        # load all these for now
        blue_bubble = ImageMan.instance.find(ImageNames.BLUEBUBBLE)
        cyan_bubble = ImageMan.instance.find(ImageNames.CYANBUBBLE)
        green_bubble = ImageMan.instance.find(ImageNames.GREENBUBBLE)
        orange_bubble = ImageMan.instance.find(ImageNames.ORANGEBUBBLE)
        pink_bubble = ImageMan.instance.find(ImageNames.PINKBUBBLE)
        self.images = [blue_bubble, cyan_bubble, green_bubble, orange_bubble, pink_bubble]

        self.base_image = choice(self.images)
        self.original_image = self.image = pygame.transform.scale(self.base_image.surface, (self.height, self.height))

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

        # gifts
        self.proba_gift = 0.05 <= randint(0, 100)/100

        # bubble type (need different classes for these)
        self.proba_multibubble = 0.05 >= randint(0, 100)/100
        self.proba_secondchance = 0.05 >= randint(0, 100)/100
        self.proba_delaybubble = 0.05 >= randint(0, 100)/100
        self.proba_spottedbubble = 0.05 >= randint(0, 100)/100
        self.proba_nukebubble = 0.05 >= randint(0, 100)/100

        # state
        self.bubble_collision_disabled = False

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
        circle_group = group.GroupMan.instance.find(group.GroupNames.CIRCLE)
        head = circle_group.nodeman.head
        while head:
            if head.pSprite.collision_enabled:
                # this is not pretty
                if head.pSprite.name == sp.BoxSpriteNames.CIRCLE \
                   and not head.pSprite.bubble_collision_disabled \
                   and pygame.sprite.collide_circle(self, head.pSprite):

                    # stats
                    explosion.multiplier += 1
                    sp.ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

                    if DEBUG:
                        print('colliding circle %s destroyed, multiplier: %d' % (head.pSprite, explosion.multiplier))

                    # multiplier font text
                    fadeout_command = timer.TimerMan.instance.find(timer.TimeEventNames.FADEOUTTOAST)
                    timer.TimerMan.instance.remove(fadeout_command)

                    font_multiplier = FontMan.instance.find(FontNames.TOAST)
                    font_multiplier.text = str('Multiplier! %d' % explosion.multiplier)
                    font_multiplier.color = InterfaceSettings.FONTCOLOR

                    # need classes for different types.. lets keep it ugly for now
                    # second chance
                    if head.pSprite.proba_secondchance:
                        head.pSprite.proba_secondchance = 0 # no more second chances for you mate
                        head.pSprite.bubble_collision_disabled = True
                        command = timer.SecondChanceBubbleCommand(head.pSprite)

                        # do it
                        timer.TimerMan.instance.add(command, 1)

                    elif head.pSprite.proba_multibubble:
                        head.pSprite.collision_enabled = False
                        command = timer.DestroySpriteCommand(head.pSprite, explosion=explosion)

                        # do it
                        timer.TimerMan.instance.add(command, 1)

                        twina = BoxSpriteMan.instance.add(BoxSpriteNames.CIRCLE,
                                                  head.pSprite.width,
                                                  max(GameSettings.BUBBLE_MAXH//4, head.pSprite.height//2),
                                                  head.pSprite.rect.centerx,
                                                  head.pSprite.rect.centery,
                                                  color=head.pSprite.color
                        )
                        twinb = BoxSpriteMan.instance.add(BoxSpriteNames.CIRCLE,
                                                  head.pSprite.width,
                                                  max(GameSettings.BUBBLE_MAXH//4, head.pSprite.height//2),
                                                  head.pSprite.rect.centerx,
                                                  head.pSprite.rect.centery,
                                                  color=head.pSprite.color
                        )
                        # delay this 
                        timer.TimerMan.instance.add(timer.AddToCircleGroupCommand(twina), GameSettings.BUBBLEPOPDELAY)
                        timer.TimerMan.instance.add(timer.AddToCircleGroupCommand(twinb), GameSettings.BUBBLEPOPDELAY)

                        # attach to wall group
                        wall_group = group.GroupMan.instance.find(group.GroupNames.WALL)
                        CollisionPairMan.instance.attach_to_group(wall_group, twina, CollisionRectPair)
                        CollisionPairMan.instance.attach_to_group(wall_group, twinb, CollisionRectPair)
                        
                        # adjust bubbles for level
                        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
                        player.level.bubbles += 2

                    elif head.pSprite.proba_delaybubble:
                        head.pSprite.collision_enabled = False
                        timer.TimerMan.instance.add(
                            timer.ColorChangeBubbleCommand(head.pSprite, 
                                                           head.pSprite.image_red, 
                                                           GameSettings.BUBBLEPOPDELAY*4
                                                           ),
                            0
                        )

                        # do it
                        command = timer.DestroySpriteCommand(head.pSprite, explosion=explosion)
                        timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY*4)

                    else: # destroy
                        head.pSprite.image = head.pSprite.image_red
                        head.pSprite.collision_enabled = False
                        command = timer.DestroySpriteCommand(head.pSprite, explosion=explosion)

                        # do it
                        timer.TimerMan.instance.add(command, GameSettings.BUBBLEPOPDELAY)

            head = head.next

    def destroy(self, explosion):
        '''
        destroy this bubble and check for neighboring collisions
        bubble might even get a second chance at life, who knows
        '''
        sp.ExplosionSprite.instance.last_collision = timer.TimerMan.instance.current_time

        # scoreboard
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        points = player.update_score(self, multiplier=explosion.multiplier)

        # show score bubble text
        font_pointsvalue = FontMan.instance.add(
            Font(FontNames.MULTIPLIER, InterfaceSettings.FONTSTYLE, 18, points, InterfaceSettings.FONTCOLOR,
                 (self.posx+self.height//2, self.posy+self.height//2)) # midpoint
        )
        timer.TimerMan.instance.add(timer.RemoveFontCommand(font_pointsvalue), 1000)

        # bubble texts
        font_bubbles = FontMan.instance.find(FontNames.BUBBLES)
        font_bubbles.text = player.level.bubbles
        font = FontMan.instance.find(FontNames.SCORE)
        font.text = player.score
        font = FontMan.instance.find(FontNames.SCOREROUND)
        font.text = player.stats_scoreround

        # sound
        self.play_sound()

        # quietly remove myself
        sp.BoxSpriteMan.instance.remove(self)
        CollisionPairMan.instance.remove(self)

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

