from bubblebuster.link import Link, Manager


class SpriteNode(Link):
    def __init__(self, sprite):
        super().__init__()
        self.pSprite = sprite

    def draw(self, screen):
        self.pSprite.draw(screen)

    def update(self):
        self.pSprite.update()

    def destroy(self):
        self.pSprite.destroy()

    def add(self, spritenode):
        self.base_add(spritenode)

    def remove(self, spritenode):
        self.base_remove(spritenode)


class SpriteNodeMan(Manager):
    def __init__(self):
        self.head = None

    def compare(self, a, b):
        return a.pSprite == b

    def remove(self, spritenode):
        assert(isinstance(spritenode, SpriteNode))
        self.base_remove(spritenode)

    def add(self, sprite):
        spritenode = SpriteNode(sprite)
        self.base_add(spritenode)
        return spritenode

    def draw(self, screen):
        head = self.head
        while head:
            head.draw(screen)
            head = head.next

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next

