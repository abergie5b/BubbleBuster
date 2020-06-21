import pygame

import game

from image import *
from sprite import *

def draw(screen):
    SpriteMan.draw(screen)

def main():
    pygame.init()

    ImageMan.create()
    ImageMan.add(ImageNames.MOUSE, 'resources/mouse.png')

    SpriteMan.create()
    SpriteMan.add(SpriteNames.MOUSE, ImageNames.MOUSE, 35, 50, 200, 200)

    # Set up the drawing window
    screen = pygame.display.set_mode((0, 0), flags=pygame.RESIZABLE)

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # the main game loop
        game.run(screen)

        # render sprites and stuff
        draw(screen)

        # update the display
        pygame.display.update()

    # Done!
    pygame.quit()

if __name__ == '__main__':
    main()

