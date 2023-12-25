import os
import sys
import pygame
from player import Hero, screen
from blocks import Platform, BlockDie, Flag
from camera import Camera, camera_configure
from menu import death_screen

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
WIN_WIDTH = 800
WIN_HEIGHT = 640

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


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


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(lvl):
    global level
    level = open(f"levels/{lvl}", encoding="utf8")
    level = level.readlines()

    x = 0
    y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "F":
                pr = Flag(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def die(hero):
    death_screen(screen)
    hero.rect.x = 50
    hero.rect.y = 50


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    animatedEntities = pygame.sprite.Group()

    n = 0
    platforms = []
    hero = Hero(all_sprites)
    entities.add(hero)

    clock = pygame.time.Clock()

    level = []

    generate_level('level1.txt')

    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    v = 240
    FPS = 60

    right = False
    left = False
    up = False
    runn = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
                hero.going_sound = False
                hero.go_sound.stop()
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False

                hero.going_sound = False
                hero.go_sound.stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                up = False

                hero.jumping_sound = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                runn = True

                hero.going_sound = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                runn = False

                hero.running_sound = False
                hero.run_sound.stop()

        screen.fill((100, 200, 100))

        all_sprites.update(left, right, up, v / FPS, runn, platforms)
        camera.update(hero)

        for e in entities:
            screen.blit(e.image, camera.apply(e))
            if isinstance(e, BlockDie):
                e.image.fill(pygame.Color((100, 200, 100)))
                e.boltAnimSpikesMove.blit(e.image, (0, 0))

        if hero.died:
            right = False
            left = False
            up = False
            runn = False
            hero.died = False

        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()
