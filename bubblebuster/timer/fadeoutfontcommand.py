from bubblebuster.timer import Command, TimeEventNames, TimerMan

class FadeOutFontCommand(Command):
    def __init__(self, font, original_color):
        self.font = font
        self.original_color = original_color
        self.name = TimeEventNames.FADEOUTTOAST

    def execute(self, delta_time):
        r = self.font.color[0]
        g = self.font.color[1]
        b = self.font.color[2]
        r = r - 1 if r else r
        g = g - 1 if g else g
        b = b - 1 if b else b
        self.font.color = (r, g, b)
        if r or g or b:
            TimerMan.instance.add(self, 1)
        else:
            self.font.color = self.original_color
            self.font.text = ''
