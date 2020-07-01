
# DEBUG
DEBUG = True

# VERSION
VERSION = 0.001


class InterfaceSettings:
    # DISPLAY SETTINGS
    if DEBUG: # windowed
        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 768
    else:
        SCREEN_WIDTH = 0 # fullscreen
        SCREEN_HEIGHT = 0
    BACKGROUND_COLOR = (0, 0, 0)

    # FONT SETTINGS
    MOUSEHIGHLIGHTFONTCOLOR = (255, 255, 255)
    FONTTITLECOLOR = (255, 255, 255)
    FONTCOLOR = (205, 205, 205)
    FONTSTYLE = 'resources/GFSCUS1D.ttf'

    # BUBBLES
    BUBBLECOLORS = ['blue', 'cyan', 'green', 'orange', 'pink']


# BUBBLE SETTINGS
NUMBER_OF_BUBBLES = 10
BUBBLE_MAXH = 200
BUBBLEPOPDELAY = 500
BUBBLE_MAXDELTA = 300

class GameSettings:
    # i dont like dis
    @staticmethod
    def init():
        # BUBBLE SETTINGS
        GameSettings.NUMBER_OF_BUBBLES = NUMBER_OF_BUBBLES
        GameSettings.BUBBLE_MAXH = BUBBLE_MAXH
        GameSettings.BUBBLEPOPDELAY = BUBBLEPOPDELAY
        GameSettings.BUBBLE_MAXDELTA = BUBBLE_MAXDELTA

