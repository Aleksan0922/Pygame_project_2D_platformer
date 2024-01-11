import pygame
from mysql.connector import connect


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 80
        self.top = 30
        self.cell_w = 30
        self.cell_h = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_w, cell_h):
        self.left = left
        self.top = top
        self.cell_w = cell_w
        self.cell_h = cell_h

    def render(self, surface):
        global screen
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(surface, pygame.Color('green'),
                                 (self.left + self.cell_w * x, self.top + self.cell_h * y,
                                  self.cell_w, self.cell_h), 1)


def show_records(player_name):
    global screen
    pygame.init()

    size = width, height = 500, 600
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    top_ten = Board(3, 10)
    top_ten.set_view(80, 80, 130, 40)

    nums = Board(1, 10)
    nums.set_view(30, 80, 40, 40)

    your_rating = Board(3, 1)
    your_rating.set_view(80, 530, 130, 40)

    your_nums = Board(1, 1)
    your_nums.set_view(30, 530, 40, 40)

    font = pygame.font.Font(None, 50)
    text = font.render("Топ 10 игроков", True, (100, 255, 100))
    text_s = font.render("Вы", True, (100, 255, 100))

    table_font = pygame.font.Font(None, 30)

    with connect(host="mysql-168777.srv.hoster.ru",
                 user="srv168777_ales09",
                 password="onclick191",
                 database="srv168777_aleks09"
                 ) as con:
        with con.cursor() as cursor:
            cursor.execute('select * from platformer_ratings order by coins desc, complete_time')
            ratings = list(cursor.fetchall())

            while len(ratings) < 10:
                ratings.append(('Нет', '', '', ''))

            fir_pl = table_font.render(ratings[0][0].ljust(25, ' ') + str(ratings[0][2]).ljust(25, ' ') +
                                       str(ratings[0][3]), True, (100, 255, 100))
            sec_pl = table_font.render(ratings[1][0].ljust(25, ' ') + str(ratings[1][2]).ljust(25, ' ') +
                                       str(ratings[1][3]), True, (100, 255, 100))
            thi_pl = table_font.render(ratings[2][0].ljust(25, ' ') + str(ratings[2][2]).ljust(25, ' ') +
                                       str(ratings[2][3]), True, (100, 255, 100))
            for_pl = table_font.render(ratings[3][0].ljust(25, ' ') + str(ratings[3][2]).ljust(25, ' ') +
                                       str(ratings[3][3]), True, (100, 255, 100))
            fit_pl = table_font.render(ratings[4][0].ljust(25, ' ') + str(ratings[4][2]).ljust(25, ' ') +
                                       str(ratings[4][3]), True, (100, 255, 100))
            six_pl = table_font.render(ratings[5][0].ljust(25, ' ') + str(ratings[5][2]).ljust(25, ' ') +
                                       str(ratings[5][3]), True, (100, 255, 100))
            sev_pl = table_font.render(ratings[6][0].ljust(25, ' ') + str(ratings[6][2]).ljust(25, ' ') +
                                       str(ratings[6][3]), True, (100, 255, 100))
            eig_pl = table_font.render(ratings[7][0].ljust(25, ' ') + str(ratings[7][2]).ljust(25, ' ') +
                                       str(ratings[7][3]), True, (100, 255, 100))
            nin_pl = table_font.render(ratings[8][0].ljust(25, ' ') + str(ratings[8][2]).ljust(25, ' ') +
                                       str(ratings[8][3]), True, (100, 255, 100))
            ten_pl = table_font.render(ratings[9][0].ljust(25, ' ') + str(ratings[9][2]).ljust(25, ' ') +
                                       str(ratings[9][3]), True, (100, 255, 100))

            cursor.execute(f'select * from platformer_ratings where player_name="{player_name}"')
            you_rating = cursor.fetchall()

            your_pl = table_font.render(you_rating[0][0].ljust(25, ' ') + str(you_rating[0][2]).ljust(25, ' ') +
                                       str(you_rating[0][3]), True, (100, 255, 100))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(text, (130, 30))
        screen.blit(text_s, (220, 490))
        screen.blit(fir_pl, (90, 90))
        screen.blit(sec_pl, (90, 130))
        screen.blit(thi_pl, (90, 170))
        screen.blit(for_pl, (90, 210))
        screen.blit(fit_pl, (90, 250))
        screen.blit(six_pl, (90, 290))
        screen.blit(sev_pl, (90, 330))
        screen.blit(eig_pl, (90, 370))
        screen.blit(nin_pl, (90, 410))
        screen.blit(ten_pl, (90, 450))
        screen.blit(your_pl, (90, 540))
        top_ten.render(screen)
        nums.render(screen)
        your_rating.render(screen)
        your_nums.render(screen)
        pygame.display.flip()
    pygame.quit()


show_records('aleks')
