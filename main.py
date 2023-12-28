import os
import sys
import pygame
from player import Hero, screen, WIN_WIDTH, WIN_HEIGHT, FONE_COLOR
from blocks import Platform, BlockDie, Flag, Coin, PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_COLOR
from camera import Camera, camera_configure
from menu import death_screen

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


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
    level_text = open(f"levels/{lvl}", encoding="utf8")
    level = level_text.readlines()
    nums = level[-2].split()
    nums = [int(n) for n in nums]
    points = level[-1].split('. ')
    points = [p.strip('(').strip(')') for p in points]
    points = [(p.split(', ')[0], p.split(', ')[1]) for p in points]
    level = level[:-2]

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
                if len(spikes) + 1 in nums:
                    bd = BlockDie(x, y, *[(eval(p[0].replace('x', str(x)).replace('y', str(y))),
                                           eval(p[1].replace('x', str(x)).replace('y', str(y))))
                                          for p in points])
                entities.add(bd)
                platforms.append(bd)
                spikes.append(bd)
            if col == "+":
                bd = BlockDie(x, y)
                bd = BlockDie(x, y, (x + 64, y), (x + 64, y + 64), (x, y + 64))
                entities.add(bd)
                platforms.append(bd)
            if col == "=":
                bd = BlockDie(x, y)
                bd = BlockDie(x, y, (x + 64, y))
                entities.add(bd)
                platforms.append(bd)
            if col == "!":
                bd = BlockDie(x, y)
                bd = BlockDie(x, y, (x, y + 64))
                entities.add(bd)
                platforms.append(bd)
            if col == "0":
                bd = BlockDie(x, y)
                bd = BlockDie(x, y, (x, y + 64), (x + 64, y + 64), (x + 64, y))
                entities.add(bd)
                platforms.append(bd)
            if col == "F":
                f = Flag(x, y)
                entities.add(f)
                platforms.append(f)
                animatedEntities.add(f)
            if col == 'C':
                coin = Coin(x, y)
                entities.add(coin)
                platforms.append(coin)
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
    spikes = []
    platforms = []
    hero = Hero(all_sprites)
    entities.add(hero)

    clock = pygame.time.Clock()

    level = []
    curr_level = 'level1.txt'

    generate_level(curr_level)

    total_level_width = (len(level[0]) - 1) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    v = 240
    FPS = 60

    font = pygame.font.Font(None, 70)
    text = font.render(f'{hero.coins_collected}', True, (10, 10, 10))
    text_x = WIN_WIDTH - text.get_width() - 40
    text_y = 20
    text_w = text.get_width()
    text_h = text.get_height()

    start_time = pygame.time.get_ticks()

    right = False
    left = False
    up = False
    runn = False

    background_sound = pygame.mixer.Sound('data/sounds/background.mp3')
    background_sound.set_volume(0.2)
    background_sound.play(-1)

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
                hero.jump_sound.stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                runn = True
                hero.going_sound = False
                hero.go_sound.stop()
            if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                runn = False
                hero.running_sound = False
                hero.run_sound.stop()

        if hero.died:
            right = False
            left = False
            up = False
            runn = False

            hero.fall_speed = 0

            death_screen(screen)

            all_sprites = pygame.sprite.Group()
            entities = pygame.sprite.Group()
            animatedEntities = pygame.sprite.Group()
            spikes = []
            platforms = []

            hero = Hero(all_sprites)
            entities.add(hero)

            generate_level(curr_level)

            total_level_width = (len(level[0]) - 1) * PLATFORM_WIDTH
            total_level_height = len(level) * PLATFORM_HEIGHT

            camera = Camera(camera_configure, total_level_width, total_level_height)

            start_time = pygame.time.get_ticks()

            hero.coins_collected = 0
            hero.rect.x = 50
            hero.rect.y = 50

            hero.died = False

        if hero.winner and hero.coins_collected > 5:
            hero.going_sound = False
            hero.running_sound = False
            hero.jumping_sound = False

            hero.go_sound.stop()
            hero.run_sound.stop()
            hero.jump_sound.stop()

            all_sprites = pygame.sprite.Group()
            entities = pygame.sprite.Group()
            animatedEntities = pygame.sprite.Group()

            platforms = []
            spikes = []

            hero = Hero(all_sprites)
            entities.add(hero)

            if curr_level == 'level2.txt':
                curr_level = 'level3.txt'
            elif curr_level == 'level1.txt':
                curr_level = 'level2.txt'
            generate_level(curr_level)

            total_level_width = (len(level[0]) - 1) * PLATFORM_WIDTH
            total_level_height = len(level) * PLATFORM_HEIGHT

            camera = Camera(camera_configure, total_level_width, total_level_height)

            start_time = pygame.time.get_ticks()

            hero.coins_collected = 0

        screen.fill(FONE_COLOR)

        all_sprites.update(left, right, up, v / FPS, runn, platforms)
        camera.update(hero)

        for e in entities:
            screen.blit(e.image, camera.apply(e))
            if isinstance(e, BlockDie):
                e.update()
                e.image.fill(pygame.Color(FONE_COLOR))
                e.animation_spikes_move.blit(e.image, (0, 0))
            if isinstance(e, Coin):
                e.image.fill(pygame.Color(FONE_COLOR))
                e.animation_coin_spin.blit(e.image, (0, 0))

        text = font.render(f'{hero.coins_collected}', True, (10, 10, 10))
        screen.blit(text, (text_x, text_y))

        curr_time = pygame.time.get_ticks()
        time = font.render(str((curr_time - start_time) // 100 / 10), True, (10, 10, 10))

        time_x = 30
        time_y = 20
        time_w = time.get_width()
        time_h = time.get_height()

        screen.blit(time, (time_x, time_y))

        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()
