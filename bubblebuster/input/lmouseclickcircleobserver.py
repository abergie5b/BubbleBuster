from bubblebuster.timer import TimerMan, ClickExplodeCommand
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import FontMan, FontNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.input import InputObserver
from bubblebuster.settings import GameSettings

class LMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.SMALLEXPLOSIONCOST:
            sound = SoundMan.instance.find(SoundNames.SMALLEXPLODE)
            sound.play()
            player.explosions -= GameSettings.SMALLEXPLOSIONCOST
            player.stats_explosions += GameSettings.SMALLEXPLOSIONCOST
            player.stats_explosionsround += GameSettings.SMALLEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs,
                                                ycurs,
                                                GameSettings.EXPLOSION_RADIUS//2,
                                                GameSettings.EXPLOSION_RADIUS_DELTA//2,
                                                GameSettings.EXPLOSION_MAX_LIVES//2
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions

