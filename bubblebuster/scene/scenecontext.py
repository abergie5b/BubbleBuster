import bubblebuster.scene as sc

class SceneContext:
    instance = None

    def __init__(self, game):
        self.game = game
        self.scene_menu = sc.SceneMenu(sc.SceneNames.MENU, game)
        self.scene_play = sc.ScenePlay(sc.SceneNames.PLAY, game)
        self.scene_over = sc.SceneOver(sc.SceneNames.OVER, game)
        self.scene_rules = sc.SceneRules(sc.SceneNames.RULES, game)
        self.scene_settings = sc.SceneSettings(sc.SceneNames.SETTINGS, game)
        self.scene_highscores = sc.SceneHighScores(sc.SceneNames.HIGHSCORES, game)
        self.scene_switch = sc.SceneSwitch(sc.SceneNames.SCENESWITCH, game)
        # start in menu
        self.scene_state = self.scene_menu
        SceneContext.instance = self
        self.scene_state.handle()
        self.scene_state.transition()

    def reset(self, player=None):
        self.scene_menu = sc.SceneMenu(sc.SceneNames.MENU, self.game)
        # preserve the player
        self.scene_play = sc.ScenePlay(sc.SceneNames.PLAY, self.game, player=player)
        self.scene_over = sc.SceneOver(sc.SceneNames.OVER, self.game)
        self.scene_rules = sc.SceneRules(sc.SceneNames.RULES, self.game)
        self.scene_settings = sc.SceneSettings(sc.SceneNames.SETTINGS, self.game)
        self.scene_highscores = sc.SceneHighScores(sc.SceneNames.HIGHSCORES, self.game)
        self.scene_switch = sc.SceneSwitch(sc.SceneNames.SCENESWITCH, self.game)

    def set_state(self, name, player=None):
        if name == sc.sc.SceneNames.MENU:
            self.scene_state = self.scene_menu 
        elif name == sc.sc.SceneNames.PLAY:
            self.scene_state = self.scene_play
        elif name == sc.sc.SceneNames.OVER:
            self.scene_state = self.scene_over
        elif name == sc.sc.SceneNames.RULES:
            self.scene_state = self.scene_rules
        elif name == sc.sc.SceneNames.SETTINGS:
            self.scene_state = self.scene_settings
        elif name == sc.sc.SceneNames.HIGHSCORES:
            self.scene_state = self.scene_highscores
        elif name == sc.sc.SceneNames.SCENESWITCH:
            self.scene_state = self.scene_switch
        else:
            raise ValueError('no matching scene state found for transition')
        self.scene_state.handle(player=player)
        self.scene_state.transition()