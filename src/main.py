
import pygame.transform
from character import Character
from game import Game
from enemy import *
import random


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    # screen.fill((0, 0, 0))
    surface = pygame.Surface((WIDTH, HEIGHT))
    enemies = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()
    game = Game(surface, enemies, fireballs)
    char = Character(surface, game)
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    keys = [pygame.K_d, pygame.K_a]

    def create_enemies():
        enemy1 = Enemy(surface, game, [random.randint(0, 700), 200])
        enemy2 = Enemy(surface, game, [random.randint(0, 700), 200])
        enemies.add(enemy1, enemy2)

    pygame.time.set_timer(pygame.USEREVENT, 4000)
    create_enemies()
    while True:
        for event in pygame.event.get():
            # print(event.__dict__)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                size = event.size
            if not game.game_over:
                if event.type == pygame.KEYDOWN and event.key in keys:
                    char.move(event.key, True)
                if event.type == pygame.KEYUP and event.key in keys:
                    char.move(event.key, False)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    char.jump()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    char.attack()
                    game.check_click(event.pos)
                if event.type == pygame.USEREVENT:
                    create_enemies()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game.game_over:
                return
                # print(clock.get_fps())

        game.blit()
        for enemy in enemies.sprites():
            enemy.update()
            enemy.blit()
        for fireball in fireballs.sprites():
            fireball.update()
            fireball.blit()
        char.blit()
        char.update()
        scaled_surface = pygame.transform.scale(surface, size)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    while True:
        main()
