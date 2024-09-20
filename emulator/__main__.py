import sys

import pygame

display = pygame.display.set_mode((64*8, 32*8))
screen = pygame.Surface((64, 32))
CAPTION = "Riton's PyChip8 Emulator"
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    display.fill((0, 0, 0))

    pygame.display.set_caption(f"{CAPTION} - {round(clock.get_fps(), 1)} fps")

    pygame.display.update()
    dt = clock.tick(60)
    

pygame.quit()
sys.exit(0)
