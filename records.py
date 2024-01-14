import pygame
from mysql.connector import connect
from player import WIN_WIDTH, WIN_HEIGHT


def show_records(player_name):
    global screen
    pygame.init()

    size = WIN_WIDTH, WIN_HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render("Топ 10 игроков", True, (100, 255, 100))

    table_font = pygame.font.Font(None, 30)
    text_back = table_font.render("Назад", True, (255, 0, 0))

    with connect(host="mysql-168777.srv.hoster.ru",
                 user="srv168777_ales09",
                 password="onclick191",
                 database="srv168777_aleks09"
                 ) as con:
        with con.cursor() as cursor:
            cursor.execute('select * from platformer_ratings order by coins desc, complete_time')
            ratings = list(cursor.fetchall())

            while len(ratings) < 10:
                ratings.append(('Нет', '', '0', '0'))

            players = []

            for i in range(len(ratings)):
                color = (100, 255, 100)
                if player_name == ratings[i][0]:
                    color = (255, 255, 100)
                pl = table_font.render(f'{i + 1}    ' + ratings[i][0].ljust(30 - len(str(ratings[i][0])), ' ') +
                                       str(ratings[i][2]).ljust(30 - len(str(ratings[i][2])), ' ') +
                                       str(ratings[i][3]), True, color)
                players.append(pl)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
        screen.fill((0, 0, 0))
        screen.blit(text, (270, 30))
        y = 90
        for p in players:
            screen.blit(p, (190, y))
            y += 40
        pygame.display.flip()
    pygame.quit()
