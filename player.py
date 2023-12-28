import os
import sys
import pygame
import pyganim
from blocks import BlockDie, Flag, Coin

WIN_WIDTH = 800
WIN_HEIGHT = 640
size = WIN_WIDTH, WIN_HEIGHT
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, WIN_WIDTH, WIN_HEIGHT)

FONE_COLOR = (150, 150, 150)

ANIMATION_SPEED = 100

ANIMATION_RIGHT = [('data/hero/right/hero.png'),
                   ('data/hero/right/hero_moving1.png'),
                   ('data/hero/right/hero_moving2.png'),
                   ('data/hero/right/hero_moving3.png'),
                   ('data/hero/right/hero_moving4.png'),
                   ('data/hero/right/hero_moving5.png'),
                   ('data/hero/right/hero_moving6.png'),
                   ('data/hero/right/hero_moving7.png'),
                   ('data/hero/right/hero_moving8.png')]
ANIMATION_LEFT = [('data/hero/left/hero.png'),
                  ('data/hero/left/hero_moving1.png'),
                  ('data/hero/left/hero_moving2.png'),
                  ('data/hero/left/hero_moving3.png'),
                  ('data/hero/left/hero_moving4.png'),
                  ('data/hero/left/hero_moving5.png'),
                  ('data/hero/left/hero_moving6.png'),
                  ('data/hero/left/hero_moving7.png'),
                  ('data/hero/left/hero_moving8.png')]

ANIMATION_STAY = [('data/hero/right/hero.png', 3)]

ANIMATION_JUMP_UP = [('data/hero/right/hero_jump_up.png', 3)]
ANIMATION_JUMP_DOWN = [('data/hero/right/hero_jump_down.png', 3)]

ANIMATION_JUMP_RIGHT_UP = [('data/hero/right/hero_jump_up.png', 3)]
ANIMATION_JUMP_RIGHT_DOWN = [('data/hero/right/hero_jump_down.png', 3)]

ANIMATION_JUMP_LEFT_UP = [('data/hero/left/hero_jump_up.png', 3)]
ANIMATION_JUMP_LEFT_DOWN = [('data/hero/left/hero_jump_down.png', 3)]

JUMP_POWER = 10
GRAVITY = 0.35

MOVE_EXTRA_SPEED = 5
JUMP_EXTRA_POWER = 1
ANIMATION_SUPER_SPEED_DELAY = 30

running = True
right = False
left = False
up = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.go_sound = pygame.mixer.Sound('data/sounds/go.mp3')
        self.run_sound = pygame.mixer.Sound('data/sounds/run.mp3')
        self.jump_sound = pygame.mixer.Sound('data/sounds/jump.mp3')
        self.jump_sound.set_volume(0.4)
        self.image = load_image('hero/right/hero1.png')
        self.rect = self.image.get_rect()
        self.going_sound = False
        self.running_sound = False
        self.jumping_sound = False
        self.run = False
        self.on_ground = False
        self.winner = False
        self.died = False
        self.coins_collected = 0
        self.speed = 0
        self.fall_speed = 0
        self.rect.y = 50
        self.rect.x = 50

        animations = []
        speed_animations = []

        for anim in ANIMATION_RIGHT:
            animations.append((anim, ANIMATION_SPEED))
            speed_animations.append((anim, ANIMATION_SUPER_SPEED_DELAY))

        self.animation_right = pyganim.PygAnimation(animations)
        self.animation_right.play()

        self.animation_speed_right = pyganim.PygAnimation(speed_animations)
        self.animation_speed_right.play()

        animations = []
        speed_animations = []

        for anim in ANIMATION_LEFT:
            animations.append((anim, ANIMATION_SPEED))
            speed_animations.append((anim, ANIMATION_SUPER_SPEED_DELAY))

        self.animation_left = pyganim.PygAnimation(animations)
        self.animation_left.play()

        self.animation_speed_left = pyganim.PygAnimation(speed_animations)
        self.animation_speed_left.play()

        self.animation_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.animation_stay.play()
        self.animation_stay.blit(self.image, (0, 0))

        self.animation_jump_left_down = pyganim.PygAnimation(ANIMATION_JUMP_LEFT_DOWN)
        self.animation_jump_left_down.play()

        self.animation_jump_right_down = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT_DOWN)
        self.animation_jump_right_down.play()

        self.animation_jump_down = pyganim.PygAnimation(ANIMATION_JUMP_DOWN)
        self.animation_jump_down.play()

        self.animation_jump_left_up = pyganim.PygAnimation(ANIMATION_JUMP_LEFT_UP)
        self.animation_jump_left_up.play()

        self.animation_jump_right_up = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT_UP)
        self.animation_jump_right_up.play()

        self.animation_jump_up = pyganim.PygAnimation(ANIMATION_JUMP_UP)
        self.animation_jump_up.play()

    def update(self, leftt, rightt, upp, spd, running, platformms):
        if upp:
            if self.on_ground:
                self.jump_sound.play()
                self.jumping_sound = True
                self.fall_speed = -JUMP_POWER
                if running and (leftt or rightt):
                    self.fall_speed -= JUMP_EXTRA_POWER
                else:
                    self.running_sound = False
                    self.run_sound.stop()
                self.image.fill(pygame.color.Color(FONE_COLOR))
                self.animation_jump_down.blit(self.image, (0, 0))
        if leftt:
            self.speed = -spd
            self.image.fill(pygame.Color(FONE_COLOR))
            if running:
                self.speed -= MOVE_EXTRA_SPEED
                if not upp:
                    if not self.running_sound:
                        self.run_sound.play(-1)
                        self.running_sound = True
                    self.animation_speed_left.blit(self.image, (0, 0))
            else:
                if not upp:
                    if not self.going_sound:
                        self.go_sound.play(-1)
                        self.going_sound = True
                    self.animation_left.blit(self.image, (0, 0))
            if upp:
                if self.fall_speed < 0:
                    if not self.jumping_sound:
                        self.jump_sound.play(1)
                        self.jumping_sound = False
                    self.animation_jump_left_up.blit(self.image, (0, 0))
                else:
                    self.jumping_sound = False
                    self.jump_sound.stop()
                    self.animation_jump_left_down.blit(self.image, (0, 0))
        if rightt:
            self.speed = spd
            self.image.fill(pygame.Color(FONE_COLOR))
            if running:
                self.speed += MOVE_EXTRA_SPEED
                if not upp:
                    if not self.running_sound:
                        self.run_sound.play(-1)
                        self.running_sound = True
                    self.animation_speed_right.blit(self.image, (0, 0))
            else:
                if not upp:
                    if not self.going_sound:
                        self.go_sound.play(-1)
                        self.going_sound = True
                    self.animation_right.blit(self.image, (0, 0))
            if upp:
                if self.fall_speed < 0:
                    if not self.jumping_sound:
                        self.jump_sound.play(1)
                        self.jumping_sound = False
                    self.animation_jump_right_up.blit(self.image, (0, 0))
                else:
                    self.jumping_sound = False
                    self.jump_sound.stop()
                    self.animation_jump_right_down.blit(self.image, (0, 0))
        if not (leftt or rightt):
            self.speed = 0
            if not upp:
                self.image.fill(pygame.Color(FONE_COLOR))
                self.animation_stay.blit(self.image, (0, 0))
                self.going_sound = False
                self.running_sound = False
                self.jumping_sound = False
                self.go_sound.stop()
                self.run_sound.stop()
                self.jump_sound.stop()
        if not self.on_ground:
            self.fall_speed += GRAVITY
        self.on_ground = False
        self.rect.y += self.fall_speed
        self.collide(0, self.fall_speed, platformms)

        self.rect.x += self.speed
        self.collide(self.speed, 0, platformms)

    def collide(self, xvel, yvel, platformss):
        for p in platformss:
            if pygame.sprite.collide_rect(self, p):
                if not isinstance(p, Flag) and not isinstance(p, BlockDie) and not isinstance(p, Coin):
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.on_ground = True
                        self.fall_speed = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.fall_speed = 0

                if isinstance(p, BlockDie):
                    self.died = True
                    self.die()

                elif isinstance(p, Flag):
                    self.winner = True

                elif isinstance(p, Coin):
                    if not p.collected:
                        self.coins_collected += 1
                        p.kill()
                        p.collected = True

    def die(self):
        self.going_sound = False
        self.running_sound = False
        self.jumping_sound = False
        self.go_sound.stop()
        self.run_sound.stop()
        self.jump_sound.stop()
