import sys

import pygame.transform

from src.character import *


def main():
    bg = pygame.image.load(f'{MEDIA}/backgrounds/bg1.jpg')
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    platform1 = pygame.image.load(f'{MEDIA}/platforms/platform2.png')
    platform1 = pygame.transform.scale(platform1, (200, 50))
    platforms = []
    for i in range(4):
        rect = pygame.rect.Rect(200*i, 550, 200, 50)
        platforms.append(rect)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    char = Character(screen, platforms)
    #char.set_run()
    clock = pygame.time.Clock()
    keys = [pygame.K_d, pygame.K_a]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in keys:
                char.move(event.key, True)
            if event.type == pygame.KEYUP and event.key in keys:
                char.move(event.key, False)


        screen.blit(bg, bg.get_rect())
        for i in range(len(platforms)):
            screen.blit(platform1, platforms[i])
        char.blit()
        char.update()
        pygame.display.update()
        i += 1
        clock.tick(60)


if __name__ == '__main__':
    main()
