
import pygame.transform
from character import Character
from game import Game
from functions import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    #screen.fill((0, 0, 0))
    surface = pygame.Surface((WIDTH, HEIGHT))
    game = Game(surface)
    char = Character(surface, game)
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    keys = [pygame.K_d, pygame.K_a]
    while True:
        for event in pygame.event.get():
            # print(event.__dict__)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                size = event.size
            if event.type == pygame.KEYDOWN and event.key in keys:
                char.move(event.key, True)
            if event.type == pygame.KEYUP and event.key in keys:
                char.move(event.key, False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                char.jump()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                char.attack()

        game.blit()
        char.blit()
        char.update()
        scaled_surface = pygame.transform.scale(surface, size)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
