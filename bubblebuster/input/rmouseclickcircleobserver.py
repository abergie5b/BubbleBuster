from bubblebuster.input import InputObserver
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.timer import TimerMan, ClickExplodeCommand
from bubblebuster.font import FontMan, FontNames
from bubblebuster.settings import GameSettings


class RMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.weapon.ammo >= player.weapon.largecost:
            sound = SoundMan.instance.find(SoundNames.LARGEEXPLODE)
            sound.play()
            player.weapon.ammo -= player.weapon.largecost
            player.stats_explosions += player.weapon.largecost
            player.stats_explosionsround += player.weapon.largecost
            click_explode = ClickExplodeCommand(xcurs,
                                                ycurs,
                                                player.weapon.radius,
                                                player.weapon.radius_delta,
                                                player.weapon.duration
                                                )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.weapon.ammo

