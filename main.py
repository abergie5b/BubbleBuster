import pygame

import game

from image import *
from sprite import *

def main():
    pygame.init()

    image_manager = ImageMan.create()
    image_manager.add(ImageNames.MOUSE, 'resources/mouse.png')

    sprite_manager = SpriteMan.create()
    sprite_manager.add(SpriteNames.MOUSE1, ImageNames.MOUSE, 35, 35, 200, 200)
    sprite_manager.add(SpriteNames.MOUSE1, ImageNames.MOUSE, 50, 50, 300, 300)
    sprite_manager.add(SpriteNames.MOUSE2, ImageNames.MOUSE, 50, 50, 400, 400)
    sprite_manager.add(SpriteNames.MOUSE2, ImageNames.MOUSE, 50, 50, 500, 500)

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
        #game.run(screen)

        # update the sprites
        sprite_manager.update()

        # clear the display
        screen.fill((0, 0, 0))

        # render sprites and stuff
        sprite_manager.draw(screen)

        # update the display
        pygame.display.update()

    # Done!
    pygame.quit()

if __name__ == '__main__':
    main()

