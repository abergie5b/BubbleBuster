from bubblebuster.input import InputObserver
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.timer import TimerMan, ClickExplodeCommand
from bubblebuster.font import FontMan, FontNames
from bubblebuster.settings import GameSettings


class RMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.LARGEEXPLOSIONCOST:
            sound = SoundMan.instance.find(SoundNames.LARGEEXPLODE)
            sound.play()
            player.explosions -= GameSettings.LARGEEXPLOSIONCOST
            player.stats_explosions += GameSettings.LARGEEXPLOSIONCOST
            player.stats_explosionsround += GameSettings.LARGEEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs,
                                                ycurs,
                                                GameSettings.EXPLOSION_RADIUS,
                                                GameSettings.EXPLOSION_RADIUS_DELTA,
                                                GameSettings.EXPLOSION_MAX_LIVES
                                                )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions
