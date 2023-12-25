import os
import sys
import pygame
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

ANIMATION_SPIKES = [('data/platforms/spikes1.png', 150),
                    ('data/platforms/spikes2.png', 150),
                    ('data/platforms/spikes3.png', 150),
                    ('data/platforms/spikes4.png', 150),
                    ('data/platforms/spikes5.png', 150),
                    ('data/platforms/spikes6.png', 150),
                    ('data/platforms/spikes7.png', 150),
                    ('data/platforms/spikes8.png', 150),
                    ('data/platforms/spikes9.png', 150),
                    ('data/platforms/spikes10.png', 150)]


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
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load_image("platforms/spikes1.png")

        self.boltAnimSpikesMove = pyganim.PygAnimation(ANIMATION_SPIKES)
        self.boltAnimSpikesMove.play()
        self.boltAnimSpikesMove.blit(self.image, (0, 0))


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("platforms/flag.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)