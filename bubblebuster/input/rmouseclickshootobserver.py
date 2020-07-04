from bubblebuster.input import InputObserver
import bubblebuster.player as pl
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.font import FontMan, FontNames


class RMouseClickShootObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        if player and player.weapon.ammo >= player.weapon.largecost:
            player.stats_explosions += player.weapon.largecost
            player.stats_explosionsround += player.weapon.largecost
            sound = SoundMan.instance.find(SoundNames.LARGEEXPLODE)
            sound.play()
            player.weapon.rshoot(xcurs, ycurs)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.weapon.stats_usedround

