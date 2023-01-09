import pygame.transform

from functions import *


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.size = self.screen.get_size()
        self.background = pygame.image.load(f'{MEDIA}/backgrounds/bg1.jpg')
        self.background = pygame.transform.scale(self.background, self.size)
        self.platform1 = pygame.image.load(f'{MEDIA}/platforms/platform2.png')
        self.platform1 = pygame.transform.scale(self.platform1, (200, 40))
        self.platforms = pygame.sprite.Group()
        self.create_platforms()
        self.resized = False
        self.gravity = 0.2

    def create_platforms(self):
        self.platforms = []
        platform_x = self.size[0]/4
        platform_y = self.size[0]/16
        self.platform1 = pygame.transform.scale(self.platform1, (platform_x, platform_y))
        for j in range(4):
            rect = pygame.rect.Rect(platform_x * j, self.size[1]-platform_y, platform_x, platform_y)
            self.platforms.append(rect)

    def resize(self, size):
        # coefficients = [new_size[0]/self.size[0], new_size[1]/self.size[1]]
        self.size = size
        self.screen = pygame.transform.scale(self.screen, self.size)

    def get_platforms(self):
        return self.platforms

    def blit_bg(self):
        self.screen.blit(self.background, self.background.get_rect())

    def blit_platforms(self):
        for j in range(len(self.platforms)):
            self.screen.blit(self.platform1, self.platforms[j])

    def blit(self):
        self.blit_bg()
        self.blit_platforms()


