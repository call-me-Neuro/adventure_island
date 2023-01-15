import pygame.transform

from functions import *


class Game:
    def __init__(self, screen, enemies, fireballs):
        self.game_over = False
        self.screen = screen
        self.enemies = enemies
        self.fireballs = fireballs
        self.size = self.screen.get_size()
        self.background = pygame.image.load(f'{MEDIA}/backgrounds/bg1.jpg')
        self.background = pygame.transform.scale(self.background, self.size)
        self.platform1 = pygame.image.load(f'{MEDIA}/platforms/platform2.png')
        self.platform1 = pygame.transform.scale(self.platform1, (200, 40))
        self.platforms = pygame.sprite.Group()
        self.create_platforms()
        self.resized = False
        self.gravity = 0.2
        self.char = None
        self.score = 0
        self.font36 = pygame.font.Font(f'{MEDIA}/fonts/ThaleahFat.ttf', 36)
        self.font72 = pygame.font.Font(f'{MEDIA}/fonts/ThaleahFat.ttf', 72)
        pygame.mixer.music.load(f"{MEDIA}/sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)
        self.hit2 = pygame.mixer.Sound(f"{MEDIA}/sounds/hit2.mp3")
        self.hit2.set_volume(0.01)
        self.miss2 = pygame.mixer.Sound(f"{MEDIA}/sounds/miss2.mp3")
        self.miss2.set_volume(0.01)
        self.hit = pygame.mixer.Sound(f"{MEDIA}/sounds/hit.mp3")
        self.hit.set_volume(0.01)
        self.miss = pygame.mixer.Sound(f"{MEDIA}/sounds/miss.mp3")
        self.miss.set_volume(0.01)
        self.boom = pygame.mixer.Sound(f"{MEDIA}/sounds/boom.mp3")
        self.boom.set_volume(0.1)
        self.music_icon = pygame.image.load(f'{MEDIA}/other/music.png')
        self.music_icon = pygame.transform.scale(self.music_icon, (50, 50))
        self.sound_icon = pygame.image.load(f'{MEDIA}/other/sound.png')
        self.sound_icon = pygame.transform.scale(self.sound_icon, (50, 50))

    def create_platforms(self):
        self.platforms = []
        platform_x = self.size[0]/4
        platform_y = self.size[0]/16
        self.platform1 = pygame.transform.scale(self.platform1, (platform_x, platform_y))
        for j in range(4):
            rect = pygame.rect.Rect(platform_x * j, self.size[1]-platform_y, platform_x, platform_y)
            self.platforms.append(rect)

    # def resize(self, size):
    #     # coefficients = [new_size[0]/self.size[0], new_size[1]/self.size[1]]
    #     self.size = size

    def get_platforms(self):
        return self.platforms

    def blit_bg(self):
        self.screen.blit(self.background, self.background.get_rect())

    def blit_platforms(self):
        for j in range(len(self.platforms)):
            self.screen.blit(self.platform1, self.platforms[j])

    def blit_score(self):
        score = self.font36.render(str(self.score), False, (255, 255, 255))
        self.screen.blit(score, (350, 50))

    def game_over_blit(self):
        text1 = self.font72.render('GAME OVER', False, (255, 255, 255))
        text2 = self.font36.render("press 'r' to start again", False, (255, 255, 255))
        self.screen.blit(text1, (230, 270))
        self.screen.blit(text2, (210, 330))

    def check_click(self, pos):
        if pygame.rect.Rect(10, 10, 50, 50).collidepoint(pos):
            if pygame.mixer.music.get_volume() == 0:
                pygame.mixer.music.set_volume(0.05)
            else:
                pygame.mixer.music.set_volume(0)

        elif pygame.rect.Rect(10, 60, 50, 50).collidepoint(pos):
            if self.boom.get_volume() == 0:
                self.boom.set_volume(0.01)
                self.hit2.set_volume(0.01)
                self.hit.set_volume(0.01)
                self.miss.set_volume(0.01)
                self.miss2.set_volume(0.01)
            else:
                self.boom.set_volume(0)
                self.hit2.set_volume(0)
                self.hit.set_volume(0)
                self.miss.set_volume(0)
                self.miss2.set_volume(0)

    def blit_icons(self):
        self.screen.blit(self.music_icon, (10, 10))
        self.screen.blit(self.sound_icon, (10, 60))

    def blit(self):
        self.blit_bg()
        self.blit_platforms()
        self.blit_score()
        self.blit_icons()
        if self.game_over:
            self.game_over_blit()


