import sys

import pygame

from emulator.cpu import CPU


display = pygame.display.set_mode((64*8, 32*8))
screen = pygame.Surface((64, 32))
CAPTION = "Riton's PyChip8 Emulator"
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()


def screen_set_pixels(display_array, surface):
    for y in range(32):
        for x in range(64):
            if display_array[y][x]:
                color = (255, 255, 255)    
            else:
                color = (0, 0, 0)
            surface.set_at((x, y), color)


cpu = CPU()
cpu.initialize_cpu()
cpu.load_fonts()
cpu.load_rom("res/IBM_Logo.ch8")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # UPDATE 
    # show fps
    pygame.display.set_caption(f"{CAPTION} - {round(clock.get_fps(), 1)} fps")

    # progress though cpu emulation at 600 instructions/second
    for instruction in range(10):   # 600 instructions / 60 FPS = 10 inst per fps
        cpu.decode()

    # DRAW
    display.fill((0, 0, 0))
    screen.fill((0, 0, 0))

    # set pixel at screen to euivalent of pixel in display array
    screen_set_pixels(cpu.display, screen)

    display.blit(pygame.transform.scale(screen, (64*8, 32*8)), (0, 0))

    pygame.display.update()
    clock.tick(1)
    

pygame.quit()
sys.exit(0)
