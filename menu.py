import pygame
import sys
import os

WIN_WIDTH = 800
WIN_HEIGHT = 640


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


class Menu:
    def __init__(self, items, screen):
        self.items = items
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.bg_color = (0, 0, 0)
        self.fg_color = (255, 255, 255)
        self.selected_color = (255, 0, 0)
        self.clock = pygame.time.Clock()
        self.items_count = len(self.items)
        self.selected = 0

    def run(self):
        while True:
            self.screen.fill(self.bg_color)
            for index, item in enumerate(self.items):
                if self.selected == index:
                    label = self.font.render(item, True, self.selected_color)
                else:
                    label = self.font.render(item, True, self.fg_color)
                width = label.get_width()
                height = label.get_height()
                pos_x = (WIN_WIDTH - width) / 2
                total_height = self.items_count * height
                pos_y = (WIN_HEIGHT - total_height) / 2 + index * height
                self.screen.blit(label, (pos_x, pos_y))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected -= 1
                    if event.key == pygame.K_DOWN:
                        self.selected += 1
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return self.selected
                    if event.key == pygame.K_ESCAPE:
                        return -1
            if self.selected < 0:
                self.selected = 0
            if self.selected >= self.items_count:
                self.selected = self.items_count - 1
            self.clock.tick(10)


def death_screen(screen):
    fon = pygame.transform.scale(load_image('backgrounds/game-over.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


def win_screen(screen):
    fon = pygame.transform.scale(load_image('backgrounds/win.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)
