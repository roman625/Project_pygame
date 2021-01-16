import pygame
import random
import pygame_gui
import os
import sqlite3


player1_cash = 1500
player2_cash = 1500
player3_cash = 1500
x_y_rect = [(600, 420, 30, 30), (570, 420, 30, 30), (540, 420, 30, 30), (510, 420, 30, 30),
            (480, 420, 30, 30), (450, 420, 30, 30), (420, 420, 30, 30), (390, 420, 30, 30),
            (360, 420, 30, 30), (330, 420, 30, 30), (300, 420, 30, 30), (300, 390, 30, 30),
            (300, 360, 30, 30), (300, 330, 30, 30), (300, 300, 30, 30), (300, 270, 30, 30),
            (300, 240, 30, 30), (300, 210, 30, 30), (300, 180, 30, 30), (300, 150, 30, 30),
            (300, 120, 30, 30), (330, 120, 30, 30), (360, 120, 30, 30), (390, 120, 30, 30),
            (420, 120, 30, 30), (450, 120, 30, 30), (480, 120, 30, 30), (510, 120, 30, 30),
            (540, 120, 30, 30), (570, 120, 30, 30), (600, 120, 30, 30), (600, 150, 30, 30),
            (600, 180, 30, 30), (600, 210, 30, 30), (600, 240, 30, 30), (600, 270, 30, 30),
            (600, 300, 30, 30), (600, 330, 30, 30), (600, 360, 30, 30), (600, 390, 30, 30)]
place_player = {'0': ['2', '3', '1']}
for i in range(1, 40+1):
    place_player[str(i)] = list()
play = '1'
pygame.init()


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


player1_roll = 0
player2_roll = 0
player3_roll = 0


class Board:
    def __init__(self):
        self.player1_color = (255, 0, 0)
        self.player2_color = (0, 255, 0)
        self.player3_color = (0, 0, 255)

    def draw_place(self, screen):
        check_winner_player()
        screen.fill((255, 255, 255))
        for i in range(120, 450, 30):
            pygame.draw.rect(screen, pygame.Color('black'), (300, i, 30, 30), 1)
            pygame.draw.rect(screen, pygame.Color('black'), (600, i, 30, 30), 1)
        for i in range(330, 630, 30):
            pygame.draw.rect(screen, pygame.Color('black'), (i, 420, 30, 30), 1)
            pygame.draw.rect(screen, pygame.Color('black'), (i, 120, 30, 30), 1)
        for i in range(0, 40):
            self.rec = list(place_player.values())
            if '1' in self.rec[i] and '2' in self.rec[i] and '3' in self.rec[i]:
                pygame.draw.rect(screen, pygame.Color(self.player3_color), (x_y_rect[i][0], x_y_rect[i][1], 30, 30))
                pygame.draw.rect(screen, pygame.Color(self.player2_color), (x_y_rect[i][0], x_y_rect[i][1], 20, 30))
                pygame.draw.rect(screen, pygame.Color(self.player1_color), (x_y_rect[i][0], x_y_rect[i][1], 10, 30))
            elif '1' in self.rec[i] and '2' in self.rec[i]:
                pygame.draw.rect(screen, pygame.Color(self.player2_color), (x_y_rect[i][0], x_y_rect[i][1], 30, 30))
                pygame.draw.rect(screen, pygame.Color(self.player1_color), (x_y_rect[i][0], x_y_rect[i][1], 15, 30))
            elif '1' in self.rec[i] and '3' in self.rec[i]:
                pygame.draw.rect(screen, pygame.Color(self.player3_color), (x_y_rect[i][0], x_y_rect[i][1], 30, 30))
                pygame.draw.rect(screen, pygame.Color(self.player1_color), (x_y_rect[i][0], x_y_rect[i][1], 15, 30))
            elif '2' in self.rec[i] and '3' in self.rec[i]:
                pygame.draw.rect(screen, pygame.Color(self.player3_color), (x_y_rect[i][0], x_y_rect[i][1], 30, 30))
                pygame.draw.rect(screen, pygame.Color(self.player2_color), (x_y_rect[i][0], x_y_rect[i][1], 15, 30))
            elif '1' in self.rec[i]:
                pygame.draw.ellipse(screen, pygame.Color(self.player1_color), x_y_rect[i])
            elif '2' in self.rec[i]:
                pygame.draw.ellipse(screen, pygame.Color(self.player2_color), x_y_rect[i])
            elif '3' in self.rec[i]:
                pygame.draw.ellipse(screen, pygame.Color(self.player3_color), x_y_rect[i])
        if play == '3':
            pygame.draw.polygon(screen, pygame.Color(0, 0, 0),
                                [[710, 340], [740, 315], [710, 290]])
        if play == '2':
            pygame.draw.polygon(screen, pygame.Color(0, 0, 0),
                                [[710, 290], [740, 265], [710, 240]])
        if play == '1':
            pygame.draw.polygon(screen, pygame.Color(0, 0, 0),
                                [[710, 240], [740, 215], [710, 190]])
        pygame.draw.ellipse(screen, pygame.Color((255, 0, 0)), (750, 200, 30, 30))
        pygame.draw.ellipse(screen, pygame.Color((0, 255, 0)), (750, 250, 30, 30))
        pygame.draw.ellipse(screen, pygame.Color((0, 0, 255)), (750, 300, 30, 30))

    def get_cell(self, mouse_pos, screen):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if x >= 50 and x <= 190 and y >= 50 and y <= 70:
            self.dice_roll(screen)
        if x >= 50 and x <= 120 and y >= 150 and y <= 170:
            self.buy_street()
        if x >= 50 and x <= 140 and y >= 250 and y <= 270:
            Sell_Field()
        if x >= 50 and x <= 140 and y >= 350 and y <= 370:
            Exchange_Field()
        if x >= 50 and x <= 170 and y >= 450 and y <= 470:
            self.buy_house()
        if x >= 750 and x <= 990 and y >= 50 and y <= 70:
            info_players()
        if x >= 750 and x <= 970 and y >= 150 and y <= 170:
            info_street()

    def dice_roll(self, screen):
        global player2_cash, player1_cash, player3_cash, play, player1_roll, player2_roll, player3_roll
        self.roll = random.choice([1, 2, 3, 4, 5, 6]) + random.choice([1, 2, 3, 4, 5, 6])
        if player1_roll == player3_roll:
            play = '1'
            player1_roll += 1
        elif player1_roll > player2_roll:
            play = '2'
            player2_roll += 1
        elif player2_roll > player3_roll:
            play = '3'
            player3_roll += 1
        for i in range(len(place_player)):
            self.rec = list(place_player.values())
            self.kek = list(place_player.keys())
            if play in self.rec[i]:
                s = place_player[f'{self.kek[i]}']
                m = s.index(play)
                del s[m]
                place_player[f'{self.kek[i]}'] = s
                if int(int(self.kek[i]) + self.roll) <= 40:
                    z = place_player[f'{int(self.kek[i]) + self.roll}']
                    z.append(play)
                    place_player[f'{int(self.kek[i]) + self.roll}'] = z
                    z = []
                    break
                elif int(int(self.kek[i]) + self.roll) >= 41:
                    if play == '1':
                        player1_cash += 200
                    if play == '2':
                        player2_cash += 200
                    if play == '3':
                        player3_cash += 200
                    z = place_player[f'{(int(self.kek[i]) + self.roll) - 41}']
                    z.append(play)
                    place_player[f'{(int(self.kek[i]) + self.roll) - 41}'] = z
                    z = []
                    break
            self.draw_place(screen)
        check_winner_player()
        self.check_place_player()

    def buy_street(self):
        global player2_cash, player1_cash, player3_cash
        for i in range(0, 40):
            self.rec = list(place_player.values())
            self.kek = list(place_player.keys())
            if play in self.rec[i]:
                con = sqlite3.connect('streets_db.sqlite')
                cur = con.cursor()
                result = cur.execute(f"""SELECT street_ FROM street WHERE position = {self.kek[i]}""")
                for el in result:
                    resul = cur.execute(f"""SELECT owner FROM street WHERE street_ = '{el[0]}'""")
                    for et in resul:
                        if et[0] is None:
                            results = cur.execute(f"""SELECT cost FROM street WHERE street_ = '{el[0]}'""")
                            for j in results:
                                if self.check_cash(int(j[0])):
                                    if play == '1':
                                        player1_cash -= int(j[0])
                                    if play == '2':
                                        player2_cash -= int(j[0])
                                    if play == '3':
                                        player3_cash -= int(j[0])
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                    SET owner = {play}
                                                    WHERE street_ = '{el[0]}'""")
                                    con.commit()
                                    con.close()
                                else:
                                    print('НЕТ ДЕНЕГ')
                        else:
                            print("Это куплено")
        check_winner_player()

    def check_cash(self, cost):
        global player2_cash, player1_cash, player3_cash
        if play == '1':
            if player1_cash - cost > 0:
                return True
        if play == '2':
            if player2_cash - cost > 0:
                return True
        if play == '3':
            if player3_cash - cost > 0:
                return True
        else:
            return False

    def buy_house(self):
        pygame.init()
        global player1_cash, player2_cash, player3_cash
        blue_street = ['mediter-ranean avenue', 'baltic avenue', 'oriental avenue',
                       'vermont avenue', 'connecticut avenue']
        pink_street = ['st. charles place', 'states avenue', 'virginia avenue',
                       'st. james place', 'tennesse avenue', 'new york avenue']
        red_street = ['kentucky avenue', 'indiana avenue', 'illinois avenue',
                      'atlantic avenue', 'ventnor avenue', 'marvin gardens']
        green_street = ['pacific avenue', 'north carolina avenue', 'pennsylvania avenue',
                        'boardwalk', 'park place']
        not_street = ['water works', 'electric company', 'reading railroad',
                      'pennsylvania railroad', 'B and Q railroad', 'short railroad']
        pygame.display.set_caption('Start')
        window_surface = pygame.display.set_mode((500, 300), 0, 32)
        b_round = pygame.Surface((500, 300))
        b_round.fill((255, 255, 255))
        manager = pygame_gui.UIManager((500, 300))
        player = '0'
        vision = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 70), (100, 50)),
            text='Показать',
            manager=manager)
        buy = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 230), (400, 50)),
            text='Построить дом',
            manager=manager)
        seller = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((150, 70), (170, 200)), manager=manager)
        sell_street = ''
        clock = pygame.time.Clock()
        run = True
        while run:
            time = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    playing_field()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        sell_street = event.text
                    if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        player = str(event.text)
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == vision:
                            con = sqlite3.connect('streets_db.sqlite')
                            cur = con.cursor()
                            result = cur.execute(f"""SELECT street_ FROM street WHERE owner = {player}""")
                            parametr = []
                            for i in result:
                                parametr.append(i[0])
                            if parametr == []:
                                parametr = ['Пусто']
                            street = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                                options_list=parametr, starting_option=f'{parametr[0]}',
                                relative_rect=pygame.Rect((10, 180), (400, 50)),
                                manager=manager)
                        if event.ui_element == buy:
                            test = ''
                            con = sqlite3.connect('streets_db.sqlite')
                            cur = con.cursor()
                            resus = cur.execute(f"""SELECT houses FROM street WHERE street_ = '{sell_street}'""")
                            for i in resus:
                                test = i[0]
                            if test <= 4 and sell_street not in not_street:
                                if sell_street in blue_street:
                                    if player == '1':
                                        player1_cash -= 50
                                    if player == '2':
                                        player3_cash -= 50
                                    if player == '3':
                                        player3_cash -= 50
                                if sell_street in pink_street:
                                    if player == '1':
                                        player1_cash -= 100
                                    if player == '2':
                                        player3_cash -= 100
                                    if player == '3':
                                        player3_cash -= 100
                                if sell_street in red_street:
                                    if player == '1':
                                        player1_cash -= 150
                                    if player == '2':
                                        player3_cash -= 150
                                    if player == '3':
                                        player3_cash -= 150
                                if sell_street in green_street:
                                    if player == '1':
                                        player1_cash -= 200
                                    if player == '2':
                                        player3_cash -= 200
                                    if player == '3':
                                        player3_cash -= 200
                                check_winner_player()
                                con = sqlite3.connect('streets_db.sqlite')
                                cur = con.cursor()
                                cur.execute(f"""UPDATE street
                                            SET houses = houses + 1
                                            WHERE street_ = '{sell_street}'""")
                                con.commit()
                                con.close()
                                kol_house = ''
                                con = sqlite3.connect('streets_db.sqlite')
                                cur = con.cursor()
                                res = cur.execute(f"""SELECT houses FROM street WHERE street_ = '{sell_street}'""")
                                for i in res:
                                    kol_house = i[0]
                                if kol_house == 1:
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                    SET payment = cost / 2 - 20
                                                    WHERE street_ = '{sell_street}'""")
                                    con.commit()
                                    con.close()
                                if kol_house == 2:
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                SET payment = cost / 2 + cost - 60
                                                WHERE street_ = '{sell_street}'""")
                                    con.commit()
                                    con.close()
                                if kol_house == 3:
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                SET payment = cost * 3
                                                WHERE street_ = '{sell_street}'""")
                                    con.commit()
                                    con.close()
                                if kol_house == 4:
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                SET payment = cost * 4 - 80
                                                WHERE street_ = '{sell_street}'""")
                                    con.commit()
                                    con.close()
                                if kol_house == 5:
                                    con = sqlite3.connect('streets_db.sqlite')
                                    cur = con.cursor()
                                    cur.execute(f"""UPDATE street
                                                SET payment = cost * 4 + 120
                                                WHERE street_ = '{sell_street}'""")
                                    con.commit()
                                    con.close()
                            playing_field()
                manager.process_events(event)
            manager.update(time)
            window_surface.blit(b_round, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

    def check_place_player(self):
        global player1_cash, player2_cash, player3_cash, play
        place_with_street = ['1', '3', '6', '8', '9', '11', '13', '14',
                             '16', '18', '19', '21', '23', '24', '26',
                             '27', '29', '28', '12', '5', '15', '25',
                             '35', '31', '32', '34', '39', '37']
        if play in self.rec[4]:
            if play == '1':
                player1_cash -= 200
            if play == '2':
                player2_cash -= 200
            if play == '3':
                player3_cash -= 200
        if play in self.rec[38]:
            if play == '1':
                player1_cash -= 100
            if play == '2':
                player2_cash -= 100
            if play == '3':
                player3_cash -= 100
        for i in range(0, 40):
            self.rec = list(place_player.values())
            self.kek = list(place_player.keys())
            if play in self.rec[i]:
                if self.kek[i] in place_with_street:
                    con = sqlite3.connect('streets_db.sqlite')
                    cur = con.cursor()
                    resultes = cur.execute(f"""SELECT owner FROM street WHERE position = {self.kek[i]}""")
                    owner_street = ''
                    for j in resultes:
                        owner_street = j[0]
                    if owner_street != play and owner_street != '' and owner_street:
                        payment = ''
                        con = sqlite3.connect('streets.db')
                        cur = con.cursor()
                        resul = cur.execute(f"""SELECT payment FROM street WHERE position = {self.kek[i]}""")
                        for k in resul:
                            payment = k[0]
                        if owner_street == '1':
                            player1_cash += int(payment)
                        if owner_street == '2':
                            player2_cash += int(payment)
                        if owner_street == '3':
                            player3_cash += int(payment)
                        if play == '1':
                            player1_cash -= int(payment)
                        if play == '2':
                            player2_cash -= int(payment)
                        if play == '3':
                            player3_cash -= int(payment)
        check_winner_player()


def check_winner_player():
    global player1_cash, player2_cash, player3_cash
    if player1_cash < 0:
        for i in range(len(place_player)):
            rec = list(place_player.values())
            kek = list(place_player.keys())
            if '1' in rec[i]:
                s = place_player[f'{kek[i]}']
                m = s.index('1')
                del s[m]
    if player2_cash < 0:
        for i in range(len(place_player)):
            rec = list(place_player.values())
            kek = list(place_player.keys())
            if '2' in rec[i]:
                s = place_player[f'{kek[i]}']
                m = s.index('2')
                del s[m]
    if player3_cash < 0:
        for i in range(len(place_player)):
            rec = list(place_player.values())
            kek = list(place_player.keys())
            if '3' in rec[i]:
                s = place_player[f'{kek[i]}']
                m = s.index('3')
                del s[m]
    players = 0
    plaer = 0
    for i in range(len(place_player)):
        rec = list(place_player.values())
        if '1' in rec[i]:
            players += 1
        if '2' in rec[i]:
            players += 1
        if '3' in rec[i]:
            players += 1
    if players == 1:
        for i in range(len(place_player)):
            rec = list(place_player.values())
            if '1' in rec[i]:
                plaer = 1
            if '2' in rec[i]:
                plaer = 2
            if '3' in rec[i]:
                plaer = 3
        screen = pygame.display.set_mode((300, 300))
        f1 = pygame.font.Font(None, 50)
        text1 = f1.render(f'Выиграл {plaer}', 1, (255, 255, 255))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.blit(text1, (50, 50))
            pygame.display.flip()
        pygame.quit()


def playing_field():
    try:
        size = 1000, 600
        screen = pygame.display.set_mode(size, 0, 32)

        class Monopoly_image(pygame.sprite.Sprite):
            def __init__(self, pos, fires):
                self.fire = fires
                super().__init__(all_sprites)
                self.image = random.choice(self.fire)
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = pos

        board = Board()
        pygame.font.SysFont('arial', 36)
        f1 = pygame.font.Font(None, 30)
        all_sprites = pygame.sprite.Group()
        running = True
        text1 = f1.render('Кинуть кубик', 1, (0, 0, 0))
        text2 = f1.render('Купить', 1, (0, 0, 0))
        text3 = f1.render('Продать', 1, (0, 0, 0))
        text4 = f1.render('Обменять', 1, (0, 0, 0))
        text5 = f1.render('Купить дома', 1, (0, 0, 0))
        text6 = f1.render('Информация об игроках', 1, (0, 0, 0))
        text7 = f1.render('Информация об улице', 1, (0, 0, 0))
        text8 = f1.render('Игрок 1', 1, (0, 0, 0))
        text9 = f1.render('Игрок 2', 1, (0, 0, 0))
        text10 = f1.render('Игрок 3', 1, (0, 0, 0))
        Monopoly_image([330, 68], [load_image("image/monopoly1.png")])
        Monopoly_image([241, 150], [load_image("image/monopoly2.png")])
        Monopoly_image([630, 150], [load_image("image/monopoly3.png")])
        Monopoly_image([330, 450], [load_image("image/monopoly4.png")])
        Monopoly_image([630, 450], [load_image("image/start.png")])
        Monopoly_image([630, 80], [load_image("image/go_out.png")])
        Monopoly_image([255, 77], [load_image("image/stop.png")])
        Monopoly_image([245, 450], [load_image("image/out.png")])
        pygame.display.update()
        while running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if running != False:
                        board.get_cell(event.pos, screen)
            screen.fill((255, 255, 255))
            board.draw_place(screen)
            screen.blit(text1, (50, 50))
            screen.blit(text2, (50, 150))
            screen.blit(text3, (50, 250))
            screen.blit(text4, (50, 350))
            screen.blit(text5, (50, 450))
            screen.blit(text6, (750, 50))
            screen.blit(text7, (750, 150))
            screen.blit(text8, (790, 210))
            screen.blit(text9, (790, 260))
            screen.blit(text10, (790, 310))
            all_sprites.draw(screen)
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()
    except pygame.error:
        pass


def info_street():
    pygame.init()
    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((500, 250), 0, 32)
    b_round = pygame.Surface((500, 250))
    b_round.fill((255, 255, 255))
    manager = pygame_gui.UIManager((500, 250))
    vision = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((190, 90), (100, 50)),
        text='Показать',
        manager=manager)
    con = sqlite3.connect('streets_db.sqlite')
    cur = con.cursor()
    result1 = cur.execute(f"""SELECT street_ FROM street""")
    parametr1 = []
    for i in result1:
        parametr1.append(i[0])
    if parametr1 == []:
        parametr1 = ['Пусто']
    street1 = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=parametr1, starting_option=f'{parametr1[0]}',
        relative_rect=pygame.Rect((150, 25), (200, 40)),
        manager=manager)
    run = True
    info_street = ''
    clock = pygame.time.Clock()
    while run:
        time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing_field()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    info_street = event.text
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == vision:
                        con = sqlite3.connect('streets_db.sqlite')
                        cur = con.cursor()
                        result = cur.execute(f"""SELECT * FROM street WHERE street_ = '{info_street}'""")
                        parametr = []
                        for i in result:
                            parametr.append(i)
                        text1 = pygame_gui.elements.ui_text_box.UITextBox(
                            html_text=f'улица {parametr[0][1]}, рента {parametr[0][3]}, владелец {parametr[0][4]}, дома {parametr[0][-1]}',
                            relative_rect=pygame.Rect((0, 200), (500, 40)),
                            manager=manager)
            manager.process_events(event)
        manager.update(time)
        window_surface.blit(b_round, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def info_players():
    global player1_cash, player2_cash, player3_cash
    pygame.init()
    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((500, 300), 0, 32)
    b_round = pygame.Surface((500, 300))
    b_round.fill((255, 255, 255))
    manager = pygame_gui.UIManager((500, 300))
    text1 = pygame_gui.elements.ui_text_box.UITextBox(
        html_text=f'{player1_cash}',
        relative_rect=pygame.Rect((0, 25), (150, 35)),
        manager=manager)
    text2 = pygame_gui.elements.ui_text_box.UITextBox(
        html_text=f'{player2_cash}',
        relative_rect=pygame.Rect((0, 75), (150, 35)),
        manager=manager)
    text3 = pygame_gui.elements.ui_text_box.UITextBox(
        html_text=f'{player3_cash}',
        relative_rect=pygame.Rect((0, 125), (150, 35)),
        manager=manager)
    con = sqlite3.connect('streets_db.sqlite')
    cur = con.cursor()
    result1 = cur.execute(f"""SELECT street_ FROM street WHERE owner = '1'""")
    parametr1 = []
    con = sqlite3.connect('streets_db.sqlite')
    cur = con.cursor()
    result2 = cur.execute(f"""SELECT street_ FROM street WHERE owner = '2'""")
    parametr2 = []
    con = sqlite3.connect('streets_db.sqlite')
    cur = con.cursor()
    result3 = cur.execute(f"""SELECT street_ FROM street WHERE owner = '3'""")
    parametr3 = []
    for i in result1:
        parametr1.append(i[0])
    if parametr1 == []:
        parametr1 = ['Пусто']
    for i in result2:
        parametr2.append(i[0])
    if parametr2 == []:
        parametr2 = ['Пусто']
    for i in result3:
        parametr3.append(i[0])
    if parametr3 == []:
        parametr3 = ['Пусто']
    street1 = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=parametr1, starting_option=f'{parametr1[0]}',
        relative_rect=pygame.Rect((150, 25), (200, 40)),
        manager=manager)
    street2 = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=parametr2, starting_option=f'{parametr2[0]}',
        relative_rect=pygame.Rect((150, 75), (200, 40)),
        manager=manager)
    street3 = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=parametr3, starting_option=f'{parametr3[0]}',
        relative_rect=pygame.Rect((150, 125), (200, 40)),
        manager=manager)
    run = True
    while run:
        time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing_field()
            manager.process_events(event)
        manager.update(time)
        window_surface.blit(b_round, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def Sell_Field():
    global player1_cash, player2_cash, player3_cash
    pygame.init()
    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((500, 300), 0, 32)
    b_round = pygame.Surface((500, 300))
    b_round.fill((255, 255, 255))
    manager = pygame_gui.UIManager((500, 300))
    player = '0'
    vision = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 70), (100, 50)),
        text='Показать',
        manager=manager)
    sell = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 230), (400, 50)),
        text='Продать',
        manager=manager)
    seller = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((150, 70), (170, 200)), manager=manager)
    sell_street = ''
    clock = pygame.time.Clock()
    run = True
    while run:
        time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing_field()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sell_street = event.text
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    player = str(event.text)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == vision:
                        con = sqlite3.connect('streets_db.sqlite')
                        cur = con.cursor()
                        result = cur.execute(f"""SELECT street_ FROM street WHERE owner = {player}""")
                        parametr = []
                        for i in result:
                            parametr.append(i[0])
                        if parametr == []:
                            parametr = ['Пусто']
                        street = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                            options_list=parametr, starting_option=f'{parametr[0]}',
                            relative_rect=pygame.Rect((10, 180), (400, 50)),
                            manager=manager)
                    if event.ui_element == sell:
                        con = sqlite3.connect('streets_db.sqlite')
                        cur = con.cursor()
                        cur.execute(f"""UPDATE street
                                    SET owner = NULL
                                    WHERE street_ = '{sell_street}'""")
                        con.commit()
                        con.close()
                        con = sqlite3.connect('streets_db.sqlite')
                        cur = con.cursor()
                        result = cur.execute(f"""SELECT cost FROM street WHERE street_ = '{sell_street}'""")
                        for i in result:
                            c = i[0]
                        if player == '1':
                            player1_cash += int(c) // 2
                        if player == '2':
                            player2_cash += int(c) // 2
                        if player == '3':
                            player3_cash += int(c) // 2
                        playing_field()
            manager.process_events(event)
        manager.update(time)
        window_surface.blit(b_round, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def Exchange_Field():
    global player1_cash, player2_cash, player3_cash
    pygame.init()
    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((500, 300))
    b_round = pygame.Surface((500, 300))
    b_round.fill((255, 255, 255))
    manager = pygame_gui.UIManager((500, 300))

    exchange = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 230), (400, 50)),
        text='Обменять',
        manager=manager)
    vision = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (200, 30)),
        text='Показать',
        manager=manager)
    seller = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((150, 70), (170, 50)), manager=manager)
    buyer = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((150, 130), (170, 50)), manager=manager)
    give = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Улица', 'Деньги'], starting_option='Деньги',
        relative_rect=pygame.Rect((10, 180), (400, 50)),
        manager=manager)
    text = pygame_gui.elements.ui_text_box.UITextBox(
        html_text='продавец',
        relative_rect=pygame.Rect((0, 65), (150, 35)),
        manager=manager)
    text1 = pygame_gui.elements.ui_text_box.UITextBox(
        html_text='покупатель',
        relative_rect=pygame.Rect((0, 125), (150, 35)),
        manager=manager)
    street_seller = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=[], starting_option='',
        relative_rect=pygame.Rect((320, 70), (170, 30)),
        manager=manager).hide()
    street_buyer = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=[], starting_option='',
        relative_rect=pygame.Rect((320, 130), (170, 30)),
        manager=manager).hide()
    cash = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((320, 130), (170, 30)), manager=manager).hide()
    player_seller = ''
    player_buyer = ''
    give_buyer = ''
    sell_street = ''
    buyer_street = ''
    buyer_cash = ''
    clock = pygame.time.Clock()
    run = True
    while run:
        time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing_field()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == give:
                        give_buyer = event.text
                    if event.ui_element == street_seller:
                        sell_street = event.text
                    if event.ui_element == street_buyer:
                        buyer_street = event.text
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == seller:
                        player_seller = str(event.text)
                    if event.ui_element == buyer:
                        player_buyer = str(event.text)
                    if event.ui_element == cash:
                        buyer_cash = str(event.text)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == vision:
                        con = sqlite3.connect('streets_db.sqlite')
                        cur = con.cursor()
                        result = cur.execute(f"""SELECT street_ FROM street WHERE owner = {player_seller}""")
                        parametr = []
                        for i in result:
                            parametr.append(i[0])
                        if parametr == []:
                            parametr = ['Пусто']
                        street_seller = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                            options_list=parametr, starting_option=parametr[0],
                            relative_rect=pygame.Rect((320, 70), (170, 30)),
                            manager=manager)
                        if give_buyer == 'Улица':
                            con = sqlite3.connect('streets_db.sqlite')
                            cur = con.cursor()
                            result = cur.execute(f"""SELECT street_ FROM street WHERE owner = {player_buyer}""")
                            parametr = []
                            for i in result:
                                parametr.append(i[0])
                            if parametr == []:
                                parametr = ['Пусто']
                            street_buyer = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                                options_list=parametr, starting_option=parametr[0],
                                relative_rect=pygame.Rect((320, 130), (170, 30)),
                                manager=manager)
                        if give_buyer == 'Деньги':
                            cash = pygame_gui.elements.UITextEntryLine(
                                relative_rect=pygame.Rect((320, 130), (170, 30)), manager=manager)
                    if event.ui_element == exchange:
                        if give_buyer == 'Улица':
                            con = sqlite3.connect('streets_db.sqlite')
                            cur = con.cursor()
                            cur.execute(f"""UPDATE street
                                            SET owner = {player_seller}
                                             WHERE street_ = '{buyer_street}'""")
                            con.commit()
                            cur.execute(f"""UPDATE street
                                            SET owner = {player_buyer}
                                            WHERE street_ = '{sell_street}'""")
                            con.commit()
                            con.close()
                        if give_buyer == 'Деньги':
                            con = sqlite3.connect('streets_db.sqlite')
                            cur = con.cursor()
                            cur.execute(f"""UPDATE street
                                            SET owner = {player_buyer}
                                            WHERE street_ = '{sell_street}'""")
                            con.commit()
                            con.close()
                            if player_seller == '1':
                                player1_cash += int(buyer_cash)
                            if player_seller == '2':
                                player2_cash += int(buyer_cash)
                            if player_seller == '3':
                                player3_cash += int(buyer_cash)
                            if player_buyer == '1':
                                player1_cash -= int(buyer_cash)
                            if player_buyer == '2':
                                player2_cash -= int(buyer_cash)
                            if player_buyer == '3':
                                player3_cash -= int(buyer_cash)
                        playing_field()
            manager.process_events(event)
        manager.update(time)
        window_surface.blit(b_round, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def clear():
    payment = ['2', '4', '6', '6', '8', '10', '10', '12', '14', '14', '16', '18', '18', '20',
               '22', '22', '24', '75', '75', '100', '100', '100', '100', '26', '26', '28', '50', '35']
    for i in range(1, 29):
        con = sqlite3.connect('streets_db.sqlite')
        cur = con.cursor()
        cur.execute(f"""UPDATE street
                    SET owner = NULL, houses = 0, payment = {payment[i - 1]}
                    WHERE id = {i}""")
        con.commit()
        con.close()


pygame.init()
clear()
WIDTH = 300
HEIGHT = 300
screen_rect = (0, 0, WIDTH, HEIGHT)
gravity = 0.25
pygame.display.set_caption('Start')
window_surface = pygame.display.set_mode((300, 300))
b_round = pygame.Surface((300, 300))
b_round.fill((255, 255, 255))
manager = pygame_gui.UIManager((300, 300))
start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 70), (100, 50)),
    text='Начать игру',
    manager=manager)


class Particle(pygame.sprite.Sprite):
    fire = [load_image("image/image1.jpg")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = gravity

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


try:
    pygame.mixer.music.load("dlya_programmy.mp3")
    pygame.mixer.music.play(-1)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    run = True
    time = clock.tick(60) / 1000.0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start:
                        playing_field()
            manager.process_events(event)
        manager.update(time)
        create_particles((150, 180))
        window_surface.blit(b_round, (0, 0))
        manager.draw_ui(window_surface)
        all_sprites.draw(window_surface)
        pygame.display.flip()
        all_sprites.update()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
except pygame.error:
    pass