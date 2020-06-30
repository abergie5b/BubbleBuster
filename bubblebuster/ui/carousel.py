from bubblebuster.sprite import BoxSpriteNames, BoxSprite, SpriteMan, SpriteNames, Sprite
from bubblebuster.font import FontMan, Font, FontNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.input import InputMan, MouseHoverHighlightRectObserver


class Carousel:
    def __init__(self, posxy, wh, windows=3):
        x, y = posxy
        w, h = wh
        #  split width by # of windows
        wwidth = w // windows
        self.rects = []
        for window in range(windows):
            rect = BoxSprite(BoxSpriteNames.BOX, wwidth, h, x, y, fill_width=2)
            self.rects.append(rect)
            x += wwidth


class WeaponCarousel(Carousel):
    def __init__(self, posxy, wh, color=(255, 255, 255), windows=3):
        super().__init__(posxy, wh, windows=windows)
        self.weapons = []

    def click(self, window):
        for _ in self.rects:
            _.selected = False
        window.selected = True

    def add_weapons(self, weapons):
        if len(weapons) != len(self.rects):
            raise ValueError('cannot create carousel with %d weapons and %d windows'
                             % (len(weapons), len(self.rects)))
        for x in range(len(weapons)):
            self.add_weapon(weapons[x], self.rects[x])

    def attach(self, player, observer):
        for x in range(len(self.rects)):
            rect = self.rects[x]
            weapon = self.weapons[x]
            InputMan.instance.lmouse.attach(observer(rect, player, weapon))
            InputMan.instance.mousecursor.attach(MouseHoverHighlightRectObserver(rect))

    def add_weapon(self, weapon, window):
        '''
        ---------------------------
        |   NAME                  |
        |   * * * * * * * * * *   |
        |   * * * * * * * * * *   |
        |   * * * I M A G E * *   |
        |   * * * * * * * * * *   |
        |   * * * * * * * * * *   |
        |   * * * * * * * * * *   |
        |   Duration              |
        |   Radius                |
        |   Radius Delta          |
        |   Cost 1                |
        |   Cost 2                |
        ---------------------------
        '''
        self.weapons.append(weapon)
        window.parent = self

        x, y = (window.posx, window.posy)
        w, h = (window.width, window.height)

        # guess at these for now
        startx = w // 4
        offsetx = w // 3
        starty = h // 10
        offsety = 20
        imagew, imageh = w//2, h//2

        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, weapon.name.name, (255, 255, 255), (x+startx, y+starty)))
        starty += offsety * 2
        sprite = SpriteMan.instance.add_sprite(Sprite(SpriteNames.NULL, weapon.image.name, imagew, imageh, x+startx, y+starty))
        starty += imageh + offsety
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, 'Duration:', (255, 255, 255), (x+startx, y+starty)))
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, weapon.duration, (255, 255, 255), (x+startx+offsetx, y+starty)))
        starty += offsety
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, 'Radius:', (255, 255, 255), (x+startx, y+starty)))
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, weapon.radius, (255, 255, 255), (x+startx+offsetx, y+starty)))
        starty += offsety
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, 'Radius Delta: ', (255, 255, 255), (x+startx, y+starty)))
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, weapon.radius_delta, (255, 255, 255), (x+startx+offsetx, y+starty)))
        starty += offsety
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, 'Normal Cost:', (255, 255, 255), (x+startx, y+starty)))
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, weapon.smallcost, (255, 255, 255), (x+startx+offsetx, y+starty)))
        starty += offsety
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, 'Special Cost:', (255, 255, 255), (x+startx, y+starty)))
        FontMan.instance.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 14, weapon.largecost, (255, 255, 255), (x+startx+offsetx, y+starty)))
        return window

