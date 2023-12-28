import os
import sys
import pygame
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (100, 100, 100)

ANIMATION_SPIKES = [('data/platforms/spikes/spikes1.png', 150),
                    ('data/platforms/spikes/spikes2.png', 150),
                    ('data/platforms/spikes/spikes3.png', 150),
                    ('data/platforms/spikes/spikes4.png', 150),
                    ('data/platforms/spikes/spikes5.png', 150),
                    ('data/platforms/spikes/spikes6.png', 150),
                    ('data/platforms/spikes/spikes7.png', 150),
                    ('data/platforms/spikes/spikes8.png', 150),
                    ('data/platforms/spikes/spikes9.png', 150),
                    ('data/platforms/spikes/spikes10.png', 150)]

ANIMATION_COINS = [('data/platforms/coins/coin1.png', 100),
                   ('data/platforms/coins/coin2.png', 100),
                   ('data/platforms/coins/coin3.png', 100),
                   ('data/platforms/coins/coin4.png', 100),
                   ('data/platforms/coins/coin5.png', 100),
                   ('data/platforms/coins/coin6.png', 100),
                   ('data/platforms/coins/coin7.png', 100),
                   ('data/platforms/coins/coin8.png', 100)]


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y, *points):
        Platform.__init__(self, x, y)
        self.image = load_image("platforms/spikes/spikes1.png")

        self.points = [(x, y), *points]
        self.curr_point = (x, y)
        self.need_point = None
        self.need_x_move = 0
        self.need_y_move = 0

        if len(self.points) > 1:
            self.need_point = self.points[0]

        self.animation_spikes_move = pyganim.PygAnimation(ANIMATION_SPIKES)
        self.animation_spikes_move.play()
        self.animation_spikes_move.blit(self.image, (0, 0))

    def update(self):
        if len(self.points) > 1:
            if self.curr_point == self.need_point:
                if self.need_point == self.points[0]:
                    self.need_point = self.points[1]
                elif self.need_point == self.points[-1]:
                    self.need_point = self.points[0]
                else:
                    self.need_point = self.points[self.points.index(self.curr_point) + 1]
                if self.curr_point[0] != self.need_point[0]:
                    if self.curr_point[0] > self.need_point[0]:
                        self.need_x_move = -1
                        self.need_y_move = 0
                    elif self.curr_point[0] < self.need_point[0]:
                        self.need_x_move = 1
                        self.need_y_move = 0
                elif self.curr_point[1] != self.need_point[1]:
                    if self.curr_point[1] > self.need_point[1]:
                        self.need_y_move = -1
                        self.need_x_move = 0
                    elif self.curr_point[1] < self.need_point[1]:
                        self.need_y_move = 1
                        self.need_x_move = 0
            self.rect.x += self.need_x_move
            self.rect.y += self.need_y_move
            self.curr_point = (self.rect.x, self.rect.y)


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("platforms/flag.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("platforms/coins/coin1.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.animation_coin_spin = pyganim.PygAnimation(ANIMATION_COINS)
        self.animation_coin_spin.play()
        self.animation_coin_spin.blit(self.image, (0, 0))
        self.collected = False
