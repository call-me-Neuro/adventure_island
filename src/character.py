import pygame.transform

from src.functions import *


class Character:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.platforms = self.get_platforms()
        self.idle = split_animated_gif(f'{MEDIA}/animations/character/__Idle.gif')
        self.run_right = split_animated_gif(f'{MEDIA}/animations/character/__Run.gif')
        self.run_left = self._load_run_left()
        self.frames = self.idle
        self.pos = [100, 100]
        self.moving_right = False
        self.moving_left = False
        self.speed = 5
        self.jumping = False
        self.rect = self.frames[0].get_rect()
        self.i = 0
        self.animation_speed = 0.5
        self.jump_speed = 5
        self.gravity = 0.2
        self.falling_speed = 3

    def get_platforms(self):
        return self.game.platforms

    def set_run(self, left):
        self.frames = self.run_left if left else self.run_right

    def jump(self):
        print(self.screen.get_size())
        if not self.not_on_the_floor():
            self.jumping = True

    def set_idle(self):
        self.frames = self.idle

    @staticmethod
    def _load_run_left():
        run_left = split_animated_gif(f'{MEDIA}/animations/character/__Run.gif')
        for img in range(len(run_left)):
            run_left[img] = pygame.transform.flip(run_left[img], True, False)
        return run_left

    def blit(self):
        self.screen.blit(self.frames[int(self.i*self.animation_speed) % len(self.frames)], self.pos)

    def move(self, key, pressed):
        if key == pygame.K_d:
            self.moving_right = True * pressed
            if pressed:
                self.set_run(False)
            else:
                if not self.moving_left:
                    self.moving_right = False
                    self.set_idle()
                else:
                    self.set_run(True)
        elif key == pygame.K_a:
            self.moving_left = True * pressed
            if pressed and not self.moving_right:
                self.set_run(True)
            else:
                if not self.moving_right:
                    self.set_idle()

    def not_on_the_floor(self):
        if self.rect.collidelist(self.platforms) == -1:
            return True
        else:
            return False

    def update(self):
        if self.game.resized:
            self.platforms = self.get_platforms()
            self.game.resized = False
        self.i += 1
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 120, 80)
        if self.jumping:
            self.pos[1] -= self.jump_speed * 2
            self.jump_speed -= self.gravity
            if self.jump_speed <= 0:
                self.jumping = False
                self.jump_speed = 5
        if self.not_on_the_floor() and not self.jumping:
            self.pos[1] += self.falling_speed
            self.falling_speed += self.gravity
        else:
            self.falling_speed = 5
        if self.moving_right and self.pos[0] < self.game.size[0] - 70:
            self.pos[0] += self.speed
        elif self.moving_left and self.pos[0] > 0 - 50:
            self.pos[0] -= self.speed
