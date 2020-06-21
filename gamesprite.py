import pygame

from image import ImageMan


class GameSprite(pygame.sprite.DirtySprite):
    def __init__(self, name, image_name, dimensions, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.width, self.height = dimensions
        self.x, self.y = position

        # attributes required by pygame
        image = ImageMan.instance.base_find(image_name).surface
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)
        
        # custom attributes
        self.delta = 2

    def wash(self):
        x = 0
        y = 0
        self.image = None
        self.rect = None
        self.mask = None
        self.delta = 0

    def move(self):
        if self.rect.x >= 1200 or self.rect.x <= 0:
            self.delta *= -1
        self.rect.x += self.delta

    def update(self):
        self.move()


class GameSpriteMan(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)


