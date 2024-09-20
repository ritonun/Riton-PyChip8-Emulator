import sys

import pygame

display = pygame.display.set_mode((64*4, 32*4))
screen = pygame.Surface((64, 32))
pygame.display.set_caption("Riton's PyChip8 Emulator")
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    display.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit(0)
