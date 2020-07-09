from bubblebuster.sound import SoundNames
import bubblebuster.scene.scene as sc
import bubblebuster.font as ft
import bubblebuster.settings as st
import bubblebuster.input as inp

class SceneOver(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # zounds
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        MENU_STARTX = st.InterfaceSettings.SCREEN_WIDTH - st.InterfaceSettings.SCREEN_WIDTH // 4
        MENU_STARTY = st.InterfaceSettings.SCREEN_HEIGHT - st.InterfaceSettings.SCREEN_HEIGHT // 6

        # back to menu
        fontmenu = self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                              st.InterfaceSettings.FONTSTYLE,
                                              24,
                                              'Back to Menu',
                                              st.InterfaceSettings.FONTCOLOR,
                                              (st.InterfaceSettings.SCREEN_WIDTH // 8, MENU_STARTY))
                                         )

        self.input_manager.mousecursor.attach(inp.MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(inp.MouseClickObserver(fontmenu, sc.SceneNames.MENU))

    def update(self):
        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

        # scene transition
        sc.SceneMan.instance.update()

    def draw(self):
        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()
