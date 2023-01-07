
import sys
import pygame.transform
from character import Character
from game import  Game
from functions import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    game = Game(screen)
    char = Character(screen, game)
    clock = pygame.time.Clock()
    keys = [pygame.K_d, pygame.K_a]
    while True:
        for event in pygame.event.get():
            # print(event.__dict__)
            if event.type == pygame.WINDOWRESIZED:
                game.resize()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in keys:
                char.move(event.key, True)
            if event.type == pygame.KEYUP and event.key in keys:
                char.move(event.key, False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                char.jump()


        game.blit()
        char.blit()
        char.update()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
