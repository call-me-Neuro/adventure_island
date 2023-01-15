import pygame.transform

from src.functions import *


class Character:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.game.char = self
        self.platforms = self.get_platforms()
        self.idle_right = split_animated_gif(f'{MEDIA}/animations/character/__Idle.gif')
        self.idle_left = self._revers_animation(self.idle_right)
        self.run_right = split_animated_gif(f'{MEDIA}/animations/character/__Run.gif')
        self.run_left = self._revers_animation(self.run_right)
        self.attack1_right = split_animated_gif(f'{MEDIA}/animations/character/__Attack1.gif')
        self.attack1_left = self._revers_animation(self.attack1_right)
        self.attack2_right = split_animated_gif(f'{MEDIA}/animations/character/__Attack2.gif')
        self.attack2_left = self._revers_animation(self.attack2_right)
        self.attacks_right = [self.attack1_right, self.attack2_right]
        self.attacks_left = [self.attack1_left, self.attack2_left]
        self.death_right = split_animated_gif(f'{MEDIA}/animations/character/__Death.gif')
        self.death_left = self._revers_animation(self.death_right)
        self.hp_image = pygame.image.load(f'{MEDIA}/other/hp.png')
        self.hp_image = pygame.transform.scale(self.hp_image, (50, 50))
        self.frames = self.idle_left
        self.model_size = (40, 50)
        self.pos = [100, 100]
        self.moving_right = False
        self.moving_left = False
        self.speed = 5
        self.jumping = False
        self.rect = self.frames[0].get_rect()
        self.i = 0
        self.animation_speed = 0.5
        self.jump_speed = 5
        self.falling_speed = 2
        self.left_direction = True
        self.attack_counter = 0
        self.attack_current = 0
        self.attack_length = 0
        self.attacking = False
        self.attack_animation_speed = 0.4
        self.attack_radius = None
        self.hp = 100
        self.attack_id = 0
        self.death = False


    def get_rect(self):
        rect = pygame.rect.Rect(self.pos[0] + 40, self.pos[1]+30, self.model_size[0], self.model_size[1])
        return rect

    def attack(self):
        if self.attacking:
            return
        self.attacking = True
        self.frames = self.attacks_left[self.attack_id] if self.left_direction else self.attacks_right[self.attack_id]
        self.attack_length = int(len(self.frames) // self.attack_animation_speed)
        attack_radius = self.get_rect()
        if self.left_direction:
            attack_radius.x -= 20
        else:
            attack_radius.x += 20
        self.attack_radius = attack_radius
        touched = False
        for enemy in self.game.enemies:
            if attack_radius.colliderect(enemy.rect):
                enemy.get_hit()
                touched = True
        if touched:
            self.game.hit.play()
        else:
            self.game.miss.play()
        self.attack_id = 0 if self.attack_id == 1 else 1

    def get_platforms(self):
        return self.game.platforms

    def set_run(self):
        self.frames = self.run_left if self.left_direction else self.run_right

    def jump(self):
        # print(self.screen.get_size())
        if self.on_the_floor():
            self.jumping = True

    def set_idle(self):
        self.frames = self.idle_left if self.left_direction else self.idle_right

    @staticmethod
    def _revers_animation(animation):
        reversed_animation = copy(animation)
        for img in range(len(reversed_animation)):
            reversed_animation[img] = pygame.transform.flip(reversed_animation[img], True, False)
        return reversed_animation

    def game_over(self):
        self.game.game_over = True
        self.hp = 0
        self.i = 0
        self.frames = self.death_left if self.left_direction else self.death_right
        self.death = True
        for enemy in self.game.enemies:
            enemy.game_over()

    def get_hit(self):
        if self.hp > 10:
            self.hp -= 10
        else:
            self.game_over()

    def blit(self):
        if self.attacking:
            self.screen.blit(self.frames[int(self.attack_current * self.attack_animation_speed)], self.pos)
        else:
            self.screen.blit(self.frames[int(self.i*self.animation_speed) % len(self.frames)], self.pos)
        self.screen.blit(self.hp_image, (650, 50))
        hp = self.game.font36.render(str(self.hp), False, (255, 255, 255))
        self.screen.blit(hp, (720, 50))

    def move(self, key, pressed):
        if key == pygame.K_d:
            if pressed:
                self.moving_right = True
                self.left_direction = False
                self.set_run()
            else:
                self.moving_right = False
                if self.moving_left:
                    self.left_direction = True
                    self.set_run()
                else:
                    self.set_idle()
        elif key == pygame.K_a:
            self.moving_left = True * pressed
            if pressed and not self.moving_right:
                self.left_direction = True
                self.set_run()
            else:
                if not self.moving_right:
                    self.set_idle()

    def on_the_floor(self):
        if self.rect.collidelist(self.platforms) == -1:
            return False
        else:
            return True

    def update(self):

        self.i += 1
        self.rect = self.get_rect()
        if self.death:
            if self.i >= len(self.death_right):
                self.frames = [self.frames[-1]]
                self.death = False
        if self.attacking:
            self.attack_current += 1
            if self.attack_current >= self.attack_length:
                if self.moving_right:
                    self.set_run()
                elif self.moving_left:
                    self.set_run()
                else:
                    self.set_idle()
                self.attack_current = 0
                self.attacking = False
        if self.jumping:
            self.pos[1] -= self.jump_speed * 2
            self.jump_speed -= self.game.gravity
            if self.jump_speed <= 0:
                self.jumping = False
                self.jump_speed = 5
        if not self.on_the_floor() and not self.jumping:
            self.pos[1] += self.falling_speed
            self.falling_speed += self.game.gravity
        else:
            self.falling_speed = 5
        if self.moving_right and self.pos[0] < self.game.size[0] - 70:
            self.pos[0] += self.speed
        elif self.moving_left and self.pos[0] > 0 - 50:
            self.pos[0] -= self.speed
