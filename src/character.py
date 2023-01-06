import pygame.transform

from Game.functions import *


class Character:
    def __init__(self, screen, platforms):
        self.screen = screen
        self.platforms = platforms
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

    def set_run(self, left):
        self.frames = self.run_left if left else self.run_right

    def set_idle(self):
        self.frames = self.idle

    def _load_run_left(self):
        run_left = split_animated_gif(f'{MEDIA}/animations/character/__Run.gif')
        for img in range(len(run_left)):
            run_left[img] = pygame.transform.flip(run_left[img], True, False)
        return run_left

    def blit(self):
        self.screen.blit(self.frames[int(self.i*self.animation_speed) % len(self.frames)], self.pos)

    def move(self, key, pressed):
        keys = pygame.key.get_pressed()
        if key == pygame.K_d:
            # if keys[pygame.K_a] and pressed:
            #     return
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

    def update(self):
        self.i += 1
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 120, 80)
        if self.rect.collidelist(self.platforms) == -1 and not self.jumping:
            self.pos[1] += self.speed
        if self.moving_right and self.pos[0] < 800 - 70:
            self.pos[0] += self.speed
        elif self.moving_left and self.pos[0] > 0 - 50:
            self.pos[0] -= self.speed
