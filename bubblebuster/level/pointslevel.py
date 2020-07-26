import bubblebuster.level as le
import bubblebuster.settings as se

class PointsLevel(le.Level):
    '''
    get a certain number of points
    '''
    def __init__(self):
        self.target_score = se.GameSettings.POINTSLEVEL_TARGETSCORE
        self.target_time = 0
        super().__init__(le.LevelNames.POINTS)
        # not used this level
        self.target_bubbles = self.bubbles

    def get_desc(self):
        return 'Get %d points!' % self.target_score

    def get_hint(self):
        return 'You might have to use multipliers wisely!'

    def update(self):
        if self.player.stats_scoreround >= self.target_score:
            self.is_complete = True
        elif self.target_bubbles <= 0 and not self.is_complete:
            self.defeat = True

    def advance(self):
        self.target_score = se.GameSettings.POINTSLEVEL_TARGETSCORE * self.level
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = self.bubbles
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()
