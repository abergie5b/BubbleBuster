import bubblebuster.level as le
import bubblebuster.settings as se


class TimeLevel(le.Level):
    '''
    destroy all the bubbles before the time limit
    '''
    def __init__(self):
        self.target_bubbles = se.GameSettings.NUMBER_OF_BUBBLES // 2
        super().__init__(le.LevelNames.TIME)

    def get_desc(self):
        return 'Pop %d bubbles within the time limit!' % (self.target_bubbles)

    def get_hint(self):
        return 'Move quickly! Watch the clock!'

    def update(self):
        if self.target_bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True
    
    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = self.bubbles // 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.target_time = max(self.max_time - self.level * 1000, 10000)
        super().advance()

