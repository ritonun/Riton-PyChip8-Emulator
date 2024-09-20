import sys

import pygame

from emulator.cpu import CPU


display = pygame.display.set_mode((64*8, 32*8))
screen = pygame.Surface((64, 32))
CAPTION = "Riton's PyChip8 Emulator"
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

cpu = CPU()
cpu.initialize_cpu()
cpu.load_fonts()
cpu.fetch_opcode()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.set_caption(f"{CAPTION} - {round(clock.get_fps(), 1)} fps")

    for y in range(32):
        for x in range(64):
            if cpu.display[y][x]:
                screen.set_at((x, y), (255, 255, 255))
            else:
                screen.set_at((x, y), (0, 0, 0))
            


    display.fill((0, 0, 0))
    screen.fill((0, 0, 0))

    display.blit(pygame.transform.scale(screen, (64*8, 32*8)), (0, 0))

    pygame.display.update()
    dt = clock.tick(60)
    

pygame.quit()
sys.exit(0)
