"""
Example of loading a background image that is not as wide as the screen, and
tiling it to fill the screen.

"""
import pygame
import random

# Initialize Pygame
pygame.init()

from pathlib import Path
assets = Path(__file__).parent / 'images'

# Set up display
screen_width = 600
screen_height = 600
scroll_speed = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tiled Background')


class MultiScreen(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((screen_width, screen_height))
        self.screen_fill = pygame.Surface((screen.get_width(), screen.get_height()))
        self.surface = pygame.Surface(((screen_width*2), screen_height))

        for x in range(0, screen.get_width(), 100):
            sa = pygame.Surface((100, screen_height))
            sa.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.screen_fill.blit(sa, (x, 0))
            print(x)
        self.image.blit(self.screen_fill, (0,0))
        self.image.blit(self.screen_fill, (screen_width, 0))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right <= screen_width:
            self.rect.x = 0

pic = MultiScreen()

sprites = pygame.sprite.Group()

sprites.add(pic)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    sprites.update()

    sprites.draw(screen)

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
