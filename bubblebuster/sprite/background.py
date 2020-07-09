import bubblebuster.settings as st

import pygame

class Background(pygame.sprite.DirtySprite):
    def __init__(self, image, posxy=(0, 0)):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.image.surface = pygame.transform.scale(self.image.surface,
                                                    (st.InterfaceSettings.SCREEN_WIDTH,
                                                     st.InterfaceSettings.SCREEN_HEIGHT)
                                                    )
        self.rect = self.image.surface.get_rect()
        self.rect.x, self.rect.y = posxy

    def draw(self, screen):
        screen.blit(self.image.surface, self.rect)
