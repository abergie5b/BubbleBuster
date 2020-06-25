from input import InputMan, LMouseClickCircleObserver, RMouseClickCircleObserver, MouseHoverHighlightObserver, MouseClickObserver, MouseClickExitObserver, MouseClickSettingsObserver
from image import ImageMan, ImageNames
from sprite import BoxSpriteMan, BoxSpriteNames, LineSprite, LineSpriteNames, SpriteMan
from collision import CollisionCirclePair, CollisionRectPair, CollisionPairMan
from timer import TimerMan
from groups import CircleGroup, Group, GroupMan, GroupNames
from factory import CircleFactory
from font import Font, FontMan, FontNames
from player import Player, PlayerMan, PlayerNames
from settings import *
from sound import Music, SoundMan, SoundNames, Sound

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
        self.sound_manager = SoundMan()

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
        SoundMan.set_active(self.sound_manager)

    def handle(self):
        raise NotImplementedError("this is an abstract class")


class SceneContext:
    instance = None

    def __init__(self, game):
        self.game = game
        self.scene_menu = SceneMenu(game)
        self.scene_play = ScenePlay(game)
        self.scene_over = SceneOver(game)
        self.scene_rules = SceneRules(game)
        self.scene_settings = SceneSettings(game)
        self.scene_highscores = SceneHighScores(game)
        # start in menu
        self.scene_state = self.scene_menu
        SceneContext.instance = self
        self.scene_state.handle()
        self.scene_state.transition()

    def reset(self):
        self.scene_menu = SceneMenu(self.game)
        self.scene_play = ScenePlay(self.game)
        self.scene_over = SceneOver(self.game)
        self.scene_rules = SceneRules(self.game)
        self.scene_settings = SceneSettings(self.game)
        self.scene_highscores = SceneHighScores(self.game)

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
        self.scene_state.handle()
        self.scene_state.transition()


class SceneMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        
        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH-100, 
                                               SCREEN_HEIGHT-100), 
                                       max_h=100
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'Bubble Buster', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//6)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 6
        MENU_STARTY = SCREEN_HEIGHT // 1.75
        MENU_OFFSETY = 45
        MENU_OFFSETX = 100

        fontplay = self.font_manager.add(Font(FontNames.PLAY, InterfaceSettings.FONTSTYLE, 32, 'Start Game', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontrules = self.font_manager.add(Font(FontNames.RULES, InterfaceSettings.FONTSTYLE, 32, 'How to Play', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

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

    def handle(self):
        SceneContext.instance.reset()
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/bubbling.wav')
        musicmenu.play()


class SceneOver(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        pass

    def handle(self):
        pass


class SceneRules(Scene):
    def __init__(self, game):
        super().__init__(game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/settings_bubbles.wav')

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        MENU_STARTX = SCREEN_WIDTH // 8
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 300
        MENU_OFFSETX_ARROW = 50

        descriptionA = 'Click to spend explosions and pop all the bubbles'
        descriptionB = 'Left click for cheap small booms, right click for expensive big booms!'
        descriptionC = 'Earn bonus for blowing up stacked bubbles'
        descriptionD = 'Get more points for popping smaller bubbles'

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionA, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionB, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionC, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionD, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Left Mouse Click', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Small Explosion', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        #MENU_STARTY += MENU_OFFSETY
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Right Mouse Click', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Large Explosion', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY + 100
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, SceneNames.MENU))

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

    def handle(self):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        musicmenu.play()

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH-100, 
                                               SCREEN_HEIGHT-100), 
                                       max_h=100
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'How to Play', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//10)
                              )
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)


class SceneSettings(Scene):
    def __init__(self, game):
        super().__init__(game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH-100,
                                               SCREEN_HEIGHT-100),
                                       max_h=100
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'Settings', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//12)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 4
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 350
        MENU_OFFSETX_ARROW = 75

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Number of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.NUMBEROFBUBBLES, InterfaceSettings.FONTSTYLE, 24, GameSettings.NUMBER_OF_BUBBLES, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        numberofbubblesup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'o', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        numberofbubblesdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'o', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Bubble Max Height', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.BUBBLESMAXH, InterfaceSettings.FONTSTYLE, 24, GameSettings.BUBBLE_MAXH, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        bubblesmaxheightup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        bubblesmaxheightdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '# of Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.NUMBEROFEXPLOSIONS, InterfaceSettings.FONTSTYLE, 24, GameSettings.PLAYER_EXPLOSIONS, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        numberofexplosionsup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        numberofexplosionsdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosion Duration', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONDURATION, InterfaceSettings.FONTSTYLE, 24, GameSettings.EXPLOSION_MAX_LIVES, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        explosiondurationup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        explosiondurationdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosion Radius', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONRADIUS, InterfaceSettings.FONTSTYLE, 24, GameSettings.EXPLOSION_RADIUS, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        explosionradiusup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        explosionradiusdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Small Explosion Cost', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.SMALLEXPLOSIONCOST, InterfaceSettings.FONTSTYLE, 24, GameSettings.SMALLEXPLOSIONCOST, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        smallexplosioncostup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        smallexplosioncostdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Large Explosion Cost', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.LARGEEXPLOSIONCOST, InterfaceSettings.FONTSTYLE, 24, GameSettings.LARGEEXPLOSIONCOST, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        largeexplosioncostup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↑', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        largeexplosioncostdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '↓', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+10)))

        MENU_STARTY += MENU_OFFSETY
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, SceneNames.MENU))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesup, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesdown, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, -10))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightup, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightdown, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, -10))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofexplosionsup, 'PLAYER_EXPLOSIONS', FontNames.NUMBEROFEXPLOSIONS, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofexplosionsdown, 'PLAYER_EXPLOSIONS', FontNames.NUMBEROFEXPLOSIONS, -1))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosiondurationup, 'EXPLOSION_MAX_LIVES', FontNames.EXPLOSIONDURATION, 5))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosiondurationdown, 'EXPLOSION_MAX_LIVES', FontNames.EXPLOSIONDURATION, -5))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosionradiusup, 'EXPLOSION_RADIUS', FontNames.EXPLOSIONRADIUS, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosionradiusdown, 'EXPLOSION_RADIUS', FontNames.EXPLOSIONRADIUS, -1))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(smallexplosioncostup, 'SMALLEXPLOSIONCOST', FontNames.SMALLEXPLOSIONCOST, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(smallexplosioncostdown, 'SMALLEXPLOSIONCOST', FontNames.SMALLEXPLOSIONCOST, -1))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(largeexplosioncostup, 'LARGEEXPLOSIONCOST', FontNames.LARGEEXPLOSIONCOST, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(largeexplosioncostdown, 'LARGEEXPLOSIONCOST', FontNames.LARGEEXPLOSIONCOST, -1))

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

    def handle(self):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        musicmenu.play()



class SceneHighScores(Scene):
    def _init(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        pass

    def handle(self):
        pass


class ScenePlay(Scene):
    def __init__(self, game):
        super().__init__(game)
        # images
        #self.image_manager.add(ImageNames.EXPLODE, 'resources/explode.png')

        # zounds
        self.sound_manager.add(SoundNames.SMALLEXPLODE, 'resources/small_explode.wav')
        self.sound_manager.add(SoundNames.LARGEEXPLODE, 'resources/large_explode.wav')

        # input
        self.input_manager.lmouse.attach(LMouseClickCircleObserver())
        self.input_manager.rmouse.attach(RMouseClickCircleObserver())


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

    def handle(self):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/bubbles.wav')
        musicmenu.play()

        # player
        player = Player(PlayerNames.PLAYERONE, 
                        GameSettings.PLAYER_EXPLOSIONS, 
                        GameSettings.PLAYER_LIVES, 
                        GameSettings.NUMBER_OF_BUBBLES
        )
        self.playerone = self.player_manager.add(player)

        # fonts
        MENU_STARTX = 10
        MENU_STARTY = 15
        MENU_OFFSETY = 20
        MENU_OFFSETX = 150

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Score: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.SCORE, InterfaceSettings.FONTSTYLE, 16, self.playerone.score, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_STARTY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Bubbles: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.BUBBLES, InterfaceSettings.FONTSTYLE, 16, GameSettings.NUMBER_OF_BUBBLES, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Explosions: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONS, InterfaceSettings.FONTSTYLE, 16, self.playerone.explosions, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Time: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_timedisplay = self.font_manager.add(Font(FontNames.TIME, InterfaceSettings.FONTSTYLE, 16, self.timer_manager.current_time, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))

        self.font_manager.add(Font(FontNames.TOAST, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (SCREEN_WIDTH-150, SCREEN_HEIGHT-25)))

        # sprites
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(GameSettings.NUMBER_OF_BUBBLES, 
                                       max_xy=(SCREEN_WIDTH-GameSettings.BUBBLE_MAXH, 
                                               SCREEN_HEIGHT-GameSettings.BUBBLE_MAXH), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

