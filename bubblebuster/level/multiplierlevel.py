import bubblebuster.level as le
import bubblebuster.settings as se


class MultiplierLevel(le.Level):
    '''
    get a high enough multiplier to pass the level
    '''
    def __init__(self):
        self.target_multiplier = 3 # should be a GameSettings
        self.target_time = 0
        super().__init__(le.LevelNames.MULTIPLIER)
        self.target_bubbles = self.bubbles

    def get_desc(self):
        return 'Get a %dx pop multiplier!' % (self.target_multiplier)

    def get_hint(self):
        return 'Take your time and wait for the bubbles to group up!'

    def update(self):
        if self.player.stats_maxmultiplierround >= self.target_multiplier:
            self.is_complete = True
        if (not self.target_bubbles or not self.player.weapon.ammo) and not self.is_complete:
            self.defeat = True

    def advance(self):
        self.target_multiplier += 1
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = self.bubbles
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        super().advance()
