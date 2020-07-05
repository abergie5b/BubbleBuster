import bubblebuster.scene.scene as sc
import bubblebuster.scene.sceneplay as scpl
import bubblebuster.scene.sceneswitch as scsw
import bubblebuster.scene.scenesetting as scst
import bubblebuster.scene.sceneweapon as scwp
import bubblebuster.scene.scenerules as scru
import bubblebuster.scene.scenemenu as scmu
#import bubblebuster.scene.sceneover as scov
import bubblebuster.scene.scenehighscore as schs

class SceneContext:
    instance = None

    def __init__(self, game):
        self.game = game
        self.scene_menu = scmu.SceneMenu(sc.SceneNames.MENU, game)
        #self.scene_over = scov.SceneOver(sc.SceneNames.OVER, game)
        self.scene_rules = scru.SceneRules(sc.SceneNames.RULES, game)
        self.scene_settings = scst.SceneSettings(sc.SceneNames.SETTINGS, game)
        self.scene_highscores = schs.SceneHighScores(sc.SceneNames.HIGHSCORES, game)
        self.scene_switch = scsw.SceneSwitch(sc.SceneNames.SCENESWITCH, game)
        self.scene_weapon = scwp.SceneWeapon(sc.SceneNames.WEAPON, game)
        self.scene_play = scpl.ScenePlay(sc.SceneNames.PLAY, game)
        # start in menu
        self.scene_state = self.scene_menu
        SceneContext.instance = self
        self.scene_state.handle()
        self.scene_state.transition()

    def reset(self):
        self.scene_menu = sc.SceneMenu(sc.SceneNames.MENU, self.game)
        self.scene_play = sc.ScenePlay(sc.SceneNames.PLAY, self.game)
        self.scene_over = sc.SceneOver(sc.SceneNames.OVER, self.game)
        self.scene_rules = sc.SceneRules(sc.SceneNames.RULES, self.game)
        self.scene_settings = sc.SceneSettings(sc.SceneNames.SETTINGS, self.game)
        self.scene_highscores = sc.SceneHighScores(sc.SceneNames.HIGHSCORES, self.game)
        self.scene_switch = sc.SceneSwitch(sc.SceneNames.SCENESWITCH, self.game)
        self.scene_weapon = sc.SceneWeapon(sc.SceneNames.WEAPON, self.game)

    def set_state(self, name):
        if name == sc.SceneNames.MENU:
            self.scene_state = self.scene_menu 
        elif name == sc.SceneNames.PLAY:
            self.scene_state = self.scene_play
        elif name == sc.SceneNames.OVER:
            self.scene_state = self.scene_over
        elif name == sc.SceneNames.RULES:
            self.scene_state = self.scene_rules
        elif name == sc.SceneNames.SETTINGS:
            self.scene_state = self.scene_settings
        elif name == sc.SceneNames.HIGHSCORES:
            self.scene_state = self.scene_highscores
        elif name == sc.SceneNames.SCENESWITCH:
            self.scene_state = self.scene_switch
        elif name == sc.SceneNames.WEAPON:
            self.scene_state = self.scene_weapon
        else:
            raise ValueError('no matching scene state found for transition')
        self.scene_state.handle()
        self.scene_state.transition()

