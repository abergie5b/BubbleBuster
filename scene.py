from input import InputMan, LMouseClickCircleObserver, RMouseClickCircleObserver, MouseHoverHighlightObserver, MouseClickObserver, MouseClickExitObserver
from image import ImageMan, ImageNames
from sprite import BoxSpriteMan, BoxSpriteNames, LineSprite, LineSpriteNames, SpriteMan
from collision import CollisionCirclePair, CollisionRectPair, CollisionPairMan
from timer import TimerMan
from groups import CircleGroup, Group, GroupMan, GroupNames
from factory import CircleFactory
from font import Font, FontMan, FontNames
from player import Player, PlayerMan, PlayerNames
from settings import *

import pygame
from enum import Enum

class SceneNames(Enum):
    MENU = 1
    PLAY = 2
    OVER = 3
    RULES = 4
    SETTINGS = 5
    HIGHSCORES = 6


class Scene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.image_manager = ImageMan()
        self.sprite_manager = SpriteMan()
        self.boxsprite_manager = BoxSpriteMan()
        self.input_manager = InputMan()
        self.group_manager = GroupMan()
        self.collisionpair_manager = CollisionPairMan()
        self.font_manager = FontMan()
        self.player_manager = PlayerMan()
        self.timer_manager = TimerMan()

        # all scenes have circle and wall groups
        self.circle_group = CircleGroup(GroupNames.CIRCLE)
        self.wall_group = Group(GroupNames.WALL)

        self.group_manager.add(self.circle_group)
        self.group_manager.add(self.wall_group)

        # all scenes have walls
        self.wall_left = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_LEFT, (0, 0), (0, SCREEN_HEIGHT), color=(255, 0, 0), width=2)
        self.wall_right = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_RIGHT, (SCREEN_WIDTH-2, 0), (SCREEN_WIDTH-2, SCREEN_HEIGHT), color=(0, 255, 0), width=2)
        self.wall_top = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_TOP, (0, 0), (SCREEN_WIDTH, 0), color=(0, 255, 255), width=2)
        self.wall_bottom = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_BOTTOM, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH, SCREEN_HEIGHT-2), color=(255, 255, 0), width=2)
        
        self.wall_group.add(self.wall_left)
        self.wall_group.add(self.wall_right)
        self.wall_group.add(self.wall_top)
        self.wall_group.add(self.wall_bottom)

    def _init(self):
        raise NotImplementedError("this is an abstract class")

    def update(self, current_time):
        raise NotImplementedError("this is an abstract class")

    def draw(self):
        raise NotImplementedError("this is an abstract class")

    def transition(self):
        ImageMan.set_active(self.image_manager)
        SpriteMan.set_active(self.sprite_manager)
        BoxSpriteMan.set_active(self.boxsprite_manager)
        InputMan.set_active(self.input_manager)
        GroupMan.set_active(self.group_manager)
        CollisionPairMan.set_active(self.collisionpair_manager)
        FontMan.set_active(self.font_manager)
        PlayerMan.set_active(self.player_manager)
        TimerMan.set_active(self.timer_manager)


class SceneContext:
    instance = None

    def __init__(self, game):
        self.game = game
        self.scene_menu = SceneMenu(game)
        self.scene_play = ScenePlay(game)
        self.scene_over = SceneOver(game)
        self.scene_rules = SceneRules(game)
        self.scene_settings = SceneSettings(game)
        # start in menu
        self.scene_state = self.scene_menu
        self.scene_state.transition()
        SceneContext.instance = self

    def reset(self):
        self.scene_menu = SceneMenu(self.game)
        self.scene_play = ScenePlay(self.game)
        self.scene_over = SceneOver(self.game)
        self.scene_rules = SceneRules(self.game)
        self.scene_settings = SceneSettings(self.game)

    def set_state(self, name):
        if name == SceneNames.MENU:
            self.scene_state = self.scene_menu 
        elif name == SceneNames.PLAY:
            self.scene_state = self.scene_play
        elif name == SceneNames.OVER:
            self.scene_state = self.scene_over
        elif name == SceneNames.RULES:
            self.scene_state = self.scene_rules
        elif name == SceneNames.SETTINGS:
            self.scene_state = self.scene_settings
        elif name == SceneNames.HIGHSCORES:
            self.scene_state = self.scene_highscores
        else:
            raise ValueError('no matching scene state found for transition')
        self.scene_state.transition()


class SceneMenu(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH-GameSettings.BUBBLE_MAXH, 
                                               SCREEN_HEIGHT-GameSettings.BUBBLE_MAXH), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   96, 
                                   'Bubble Busters', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//6)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 6
        MENU_STARTY = SCREEN_HEIGHT // 1.75
        MENU_OFFSETY = 45
        MENU_OFFSETX = 100

        fontplay = self.font_manager.add(Font(FontNames.PLAY, InterfaceSettings.FONTSTYLE, 32, 'Play', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontrules = self.font_manager.add(Font(FontNames.RULES, InterfaceSettings.FONTSTYLE, 32, 'Rules', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontsettings = self.font_manager.add(Font(FontNames.SETTINGS, InterfaceSettings.FONTSTYLE, 32, 'Settings', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fonthighscores = self.font_manager.add(Font(FontNames.HIGHSCORES, InterfaceSettings.FONTSTYLE, 32, 'High Scores', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontexit = self.font_manager.add(Font(FontNames.EXIT, InterfaceSettings.FONTSTYLE, 32, 'Exit', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.lmouse.attach(MouseClickObserver(fontplay, SceneNames.PLAY))
        self.input_manager.lmouse.attach(MouseClickObserver(fontrules, SceneNames.RULES))
        self.input_manager.lmouse.attach(MouseClickObserver(fontsettings, SceneNames.SETTINGS))
        self.input_manager.lmouse.attach(MouseClickObserver(fonthighscores, SceneNames.HIGHSCORES))
        self.input_manager.lmouse.attach(MouseClickExitObserver(fontexit, None))
        #self.input_manager.rmouse.attach(RMouseClickCircleObserver())

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontplay, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontrules, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontsettings, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fonthighscores, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontexit, None))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

    def update(self):
        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

    def draw(self):
        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)


class SceneOver(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        pass


class SceneRules(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        pass


class SceneSettings(Scene):
    def __init__(self, game):
        super().__init__(game)

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH-GameSettings.BUBBLE_MAXH, 
                                               SCREEN_HEIGHT-GameSettings.BUBBLE_MAXH), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'Settings', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//10)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 4
        MENU_STARTY = SCREEN_HEIGHT // 4
        MENU_OFFSETY = 45
        MENU_OFFSETX = 100

        numberofbubbles = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Number of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        bubblesmaxheight = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Bubble Max Height', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        numberofexplosions = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, '# of Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        explosionduration = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Explosion Duration', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        explosionradius = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Explosion Radius', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        smallexplosioncost = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Small Explosion Cost', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        largeexplosioncost = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Large Explosion Cost', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, SceneNames.MENU))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)


    def update(self):
        # font
        self.font_manager.update()

        # sprites
        self.boxsprite_manager.update()

        # input
        self.input_manager.update(self.game)

        # collisions
        self.collisionpair_manager.process()

    def draw(self):
        self.boxsprite_manager.draw(self.screen)
        self.font_manager.draw(self.screen)


class SceneHighScores(Scene):
    def _init(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        pass


class ScenePlay(Scene):
    def __init__(self, game):
        super().__init__(game)
        # images
        #self.image_manager.add(ImageNames.EXPLODE, 'resources/explode.png')

        # sprites
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(GameSettings.NUMBER_OF_BUBBLES, 
                                       max_xy=(SCREEN_WIDTH-GameSettings.BUBBLE_MAXH, 
                                               SCREEN_HEIGHT-GameSettings.BUBBLE_MAXH), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        # input
        self.input_manager.lmouse.attach(LMouseClickCircleObserver())
        self.input_manager.rmouse.attach(RMouseClickCircleObserver())

        # player
        player = Player(PlayerNames.PLAYERONE, GameSettings.PLAYER_EXPLOSIONS, GameSettings.PLAYER_LIVES, GameSettings.NUMBER_OF_BUBBLES)
        self.playerone = self.player_manager.add(player)

        # fonts
        MENU_STARTX = 10
        MENU_STARTY = 15
        MENU_OFFSETY = 15
        MENU_OFFSETX = 100
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Explosions: ', (255, 255, 255), (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONS, InterfaceSettings.FONTSTYLE, 16, self.playerone.explosions, (255, 255, 255), (MENU_OFFSETX, MENU_STARTY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Lives: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.LIVES, InterfaceSettings.FONTSTYLE, 16, self.playerone.lives, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Score: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.SCORE, InterfaceSettings.FONTSTYLE, 16, self.playerone.score, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Multiplier: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.MULTIPLIER_TITLE, InterfaceSettings.FONTSTYLE, 16, 0, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Bubbles: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.BUBBLES, InterfaceSettings.FONTSTYLE, 16, GameSettings.NUMBER_OF_BUBBLES, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Time: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_timedisplay = self.font_manager.add(Font(FontNames.TIME, InterfaceSettings.FONTSTYLE, 16, self.timer_manager.current_time, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

    def update(self):
        time = pygame.time.get_ticks()

        # input updates
        self.input_manager.update(self.game)

        # update the sprites
        self.sprite_manager.update()
        self.boxsprite_manager.update()

        # update the timer events
        self.timer_manager.update(self, time)

        # fonts
        # poo poo
        self.font_timedisplay.text = '%s.%s' % (time // 1000, str(time)[-3:-1])
        self.font_manager.update()

        # update collision events
        self.collisionpair_manager.process()

        # player
        self.player_manager.update()

    def draw(self):
        # render sprites and stuff
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # fonts
        self.font_manager.draw(self.screen)

