import bubblebuster.player as pl
from bubblebuster.font import FontMan, FontNames
from bubblebuster.sound import SoundMan, SoundNames
from bubblebuster.input import InputObserver

class LMouseClickShootObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        if player and player.weapon.ammo >= player.weapon.smallcost:
            player.stats_explosions += player.weapon.smallcost
            player.stats_explosionsround += player.weapon.smallcost
            sound = SoundMan.instance.find(SoundNames.SMALLEXPLODE)
            sound.play()
            player.weapon.lshoot(xcurs, ycurs)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.weapon.stats_usedround

