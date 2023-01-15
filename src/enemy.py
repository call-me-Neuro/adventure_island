from functions import *
from fireball import Fireball


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, game, pos):
        super().__init__()
        self.screen = screen
        self.game = game
        self.pos = pos
        self.run_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Run.png', 8)
        self.run_left = self._revers_animation(self.run_right)
        self.death_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Death.png', 6)
        self.death_left = self._revers_animation(self.death_right)
        self.attack1_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Attack1.png', 6)
        self.attack1_left = self._revers_animation(self.attack1_right)
        self.attack2_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Attack2.png', 6)
        self.attack2_left = self._revers_animation(self.attack2_right)
        self.take_hit_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Take Hit.png', 4)
        self.take_hit_left = self._revers_animation(self.take_hit_right)
        self.idle_right = get_animation_sheet2(f'{MEDIA}/animations/char2/Idle.png', 8)
        self.idle_left = self._revers_animation(self.idle_right)
        self.frames = self.run_left
        self.moving_right = False
        self.moving_left = False
        self.left_direction = False
        self.platforms = self.get_platforms()
        self.model_size = (50, 50)
        self.i = 0
        self.animation_speed = 0.3
        self.falling_speed = 2
        self.rect = self.get_rect()
        self.speed = 1
        self.death = False
        self.death_counter = 0
        self.fireball_cooldown = 5
        self.attacking = False
        self.attack_current = 0
        self.attack_animation_speed = 0.2
        self.attack_length = 0
        self.attack_radius = None
        self.attacking_pause = False
        self.hp = 2
        self.get_hit_anim = False


        self.created_fireball = False

    def create_fireball(self):
        fireball = Fireball(self.screen, self.game, self.pos, self.left_direction)
        self.game.fireballs.add(fireball)
        self.created_fireball = True

    def get_rect(self):
        rect = pygame.rect.Rect(self.pos[0]+70, self.pos[1]+20, self.model_size[0], self.model_size[1])
        return rect

    def game_over(self):
        self.frames = self.idle_left if self.left_direction else self.idle_right
        self.attacking = False

    def get_hit(self):
        if self.death:
            return
        self.i = 0
        self.animation_speed = 0.1
        self.hp -= 1
        if self.hp > 0:
            self.get_hit_anim = True
            self.frames = self.take_hit_left if self.left_direction else self.take_hit_right
        else:
            self.death = True
            self.get_hit_anim = False
            self.attacking = False
            self.frames = self.death_left if self.left_direction else self.death_right
            self.game.score += 10

    def blit(self):
        if self.attacking:
            self.screen.blit(self.frames[int(self.attack_current * self.attack_animation_speed) % len(self.frames)], self.pos)
        else:
            self.screen.blit(self.frames[int(self.i * self.animation_speed) % len(self.frames)], self.pos)

    def on_the_floor(self):
        if self.rect.collidelist(self.platforms) == -1:
            return False
        else:
            return True

    def get_platforms(self):
        return self.game.platforms

    def attack(self):
        if self.attacking_pause or self.attacking:
            return
        self.attacking_pause = True
        self.i = 0
        self.attack_length = int(len(self.attack1_right) // self.attack_animation_speed)
        attack_radius = self.get_rect()
        if self.left_direction:
            attack_radius.width += 40
            attack_radius.x -= 60
        else:
            attack_radius.width += 40
            attack_radius.x += 20
        self.attack_radius = attack_radius

    def hit(self):
        self.attacking = True
        self.frames = self.attack1_left if self.left_direction else self.attack1_right
        touched = False
        if self.attack_radius.colliderect(self.game.char.rect):
            self.game.char.get_hit()
            touched = True
        if touched:
            self.game.hit2.play()
        else:
            self.game.miss2.play()

    def follow(self):
        if self.on_the_floor():
            if self.game.char.rect.x > self.rect.x:
                self.moving_right = True
                self.moving_left = False
                self.frames = self.run_right
                self.left_direction = False
            else:
                self.moving_left = True
                self.moving_right = False
                self.frames = self.run_left
                self.left_direction = True
            if abs(self.game.char.rect.x - self.rect.x) < 80:
                self.attack()

    def update(self):
        self.i += 1
        self.rect = self.get_rect()
        if not self.on_the_floor():
            self.pos[1] += self.falling_speed
            self.falling_speed += self.game.gravity
        else:
            self.falling_speed = 5
        if not self.game.game_over:
            if self.attacking and not self.death and not self.get_hit_anim:
                self.attack_current += 1
                if self.attack_current >= self.attack_length:
                    self.attack_current = 0
                    self.attacking = False
            if self.attacking_pause:
                if self.attack_radius is not None:
                    pygame.draw.rect(self.screen, (255, 255, 215), self.attack_radius, 1)
                if self.i >= 30:
                    self.attacking_pause = False
                    self.hit()
            if self.death:
                if self.i >= 50:
                    self.game.enemies.remove(self)
            if self.get_hit_anim:
                if self.i >= 30:
                    self.get_hit_anim = False
            if not self.death and not self.attacking and not self.attacking_pause:
                self.follow()

            if self.moving_right and self.pos[0] < self.game.size[0] - 70 and not self.death and not self.attacking_pause \
                    and not self.attacking:
                self.pos[0] += self.speed
            elif self.moving_left and self.pos[0] > 0 - 50 and not self.death and not self.attacking_pause \
                    and not self.attacking:
                self.pos[0] -= self.speed
            if not self.created_fireball:
                if self.on_the_floor():
                    self.create_fireball()

    @staticmethod
    def _revers_animation(animation):
        reversed_animation = copy(animation)
        for img in range(len(reversed_animation)):
            reversed_animation[img] = pygame.transform.flip(reversed_animation[img], True, False)
        return reversed_animation
