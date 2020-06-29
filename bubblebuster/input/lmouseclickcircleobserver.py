from bubblebuster.timer import TimerMan, ClickExplodeCommand
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import FontMan, FontNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.input import InputObserver
from bubblebuster.settings import GameSettings

class LMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.weapon.ammo >= player.weapon.smallcost:
            sound = SoundMan.instance.find(SoundNames.SMALLEXPLODE)
            sound.play()
            player.weapon.ammo -= player.weapon.smallcost
            player.stats_explosions += player.weapon.smallcost
            player.stats_explosionsround += player.weapon.smallcost
            click_explode = ClickExplodeCommand(xcurs,
                                                ycurs,
                                                player.weapon.radius//2,
                                                player.weapon.radius_delta//2,
                                                player.weapon.duration//2
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.weapon.ammo

