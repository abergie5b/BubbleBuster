import bubblebuster.sprite as sp


class WallSprite(sp.LineSprite):
    def accept(self, circle):
        if self.name == sp.LineSpriteNames.WALL_LEFT or self.name == sp.LineSpriteNames.WALL_RIGHT: # vertical
            circle.deltax *= -1
        else:  # if it is a horizontal line
            circle.deltay *= -1

        # why do need to call this twice huh?
        circle.move()
        circle.update()
