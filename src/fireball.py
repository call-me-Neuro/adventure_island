import pygame.sprite

from functions import *


class Fireball(pygame.sprite.Sprite):

    def __init__(self, screen, game, pos, left_direction):
        super().__init__()
        self.screen = screen
        self.game = game
        self.pos = [pos[0], pos[1]+30]
        self.left_direction = left_direction
        self.right_animation = split_animated_gif(f'{MEDIA}/animations/char2/fireball.gif')
        self.left_animation = self._revers_animation(self.right_animation)
        self.frames = self.left_animation if self.left_direction else self.right_animation
        self.animation_speed = 0.2
        self.i = 0
        self.speed = 2
        self.model_size = (30, 30)
        self.rect = self.get_rect()


    def get_rect(self):
        rect = pygame.rect.Rect(self.pos[0]+30, self.pos[1], self.model_size[0], self.model_size[1])
        return rect

    def blit(self):
        self.screen.blit(self.frames[int(self.i * self.animation_speed) % len(self.frames)], self.pos)
        # pygame.draw.rect(self.screen, (255, 255, 215), self.rect, 1)

    @staticmethod
    def _revers_animation(animation):
        reversed_animation = copy(animation)
        for img in range(len(reversed_animation)):
            reversed_animation[img] = pygame.transform.flip(reversed_animation[img], True, False)
        return reversed_animation

    def update(self):
        self.rect = self.get_rect()
        self.i += 1
        if self.left_direction:
            self.pos[0] -= self.speed
        else:
            self.pos[0] += self.speed
        if self.rect.colliderect(self.game.char.rect):
            self.game.char.get_hit()
            self.game.boom.play()
            self.game.fireballs.remove(self)
        if self.pos[0] > self.game.size[0] or self.pos[0]+self.rect.width < 0:
            self.game.fireballs.remove(self)
