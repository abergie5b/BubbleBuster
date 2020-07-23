from bubblebuster.input import InputObserver
import bubblebuster.font as fo

class ToggleStatsObserver(InputObserver):

    def notify(self, screen, xcurs, ycurs):
        fontlevel = fo.FontMan.instance.find(fo.FontNames.LEVEL)
        fontlevellabel = fo.FontMan.instance.find(fo.FontNames.CURRENTLEVEL)
        fontscoreround = fo.FontMan.instance.find(fo.FontNames.SCOREROUND)
        fontscoreroundlabel = fo.FontMan.instance.find(fo.FontNames.SCOREROUNDLABEL)
        fontscore = fo.FontMan.instance.find(fo.FontNames.SCORE)
        fontscorelabel = fo.FontMan.instance.find(fo.FontNames.SCORELABEL)
        fontbubbles = fo.FontMan.instance.find(fo.FontNames.BUBBLES)
        fontbubbleslabel = fo.FontMan.instance.find(fo.FontNames.BUBBLESLABEL)
        fontexplosions = fo.FontMan.instance.find(fo.FontNames.EXPLOSIONS)
        fontexplosionslabel = fo.FontMan.instance.find(fo.FontNames.EXPLOSIONSLABEL)
        fonttime = fo.FontMan.instance.find(fo.FontNames.TIME)
        fonttimelabel = fo.FontMan.instance.find(fo.FontNames.TIMELABEL)
        
        fontlevel.is_draw_enabled ^= True
        fontlevellabel.is_draw_enabled ^= True
        fontscoreround.is_draw_enabled ^= True
        fontscoreroundlabel.is_draw_enabled ^= True
        fontscore.is_draw_enabled ^= True
        fontscorelabel.is_draw_enabled ^= True
        fontbubbles.is_draw_enabled ^= True
        fontbubbleslabel.is_draw_enabled ^= True
        fontexplosions.is_draw_enabled ^= True
        fontexplosionslabel.is_draw_enabled ^= True
        fonttime.is_draw_enabled ^= True
        fonttimelabel.is_draw_enabled ^= True
