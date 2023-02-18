import pygame
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

FPS = 50
pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.play(-1)

global flag_level, hp
flag_level = False
hp = 10000


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

tile_images = {
    'wall': pygame.transform.scale(load_image('block.png'), (screen.get_width() // 31, screen.get_height() // 18)),
    'portal': pygame.transform.scale(load_image('portal.png'), (screen.get_width() // 31, screen.get_height() // 18)),
    'empty': pygame.transform.scale(load_image('water22.jpg'), (screen.get_width() // 31, screen.get_height() // 18)),
    'other': pygame.transform.scale(load_image('water22.jpg'), (screen.get_width() // 31, screen.get_height() // 18)),
    'enemy2': pygame.transform.scale(load_image('enemy1.png'), (screen.get_width() // 31, screen.get_height() // 18)),
    'enemy1': pygame.transform.scale(load_image('enemy2.png'), (screen.get_width() // 31, screen.get_height() // 18)),
    'enemy3': pygame.transform.scale(load_image('enemy3.gif'), (screen.get_width() // 31, screen.get_height() // 18))
}


def start_screen():
    intro_text = ["ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ПУТЬ ИЗ ЛЕСА' ", "",
                  "Правила игры",
                  "Вам предстоит выбрать героя, далее пройти несколько уровней.",
                  "Чтобы перейти на новый уровень нужно убить всех злодеев и пройти в портал.",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def choose_character():
    global tile_images
    #start = pygame.sprite.Group()

    intro_text = ['CHOOSE YOUR CHARACTER']

    fon = pygame.transform.scale(load_image('black.png'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    string_rendered = font.render(intro_text[0], 100, pygame.Color('white'))
    screen.blit(string_rendered, ((screen.get_width() - 796) // 2, 70, 896, 125))
    player1 = pygame.transform.scale(load_image('player2.png'), (200, 200))
    #start.add(player1)
    player1_rect = player1.get_rect(bottomleft=(screen.get_width() // 3 - 200, 500))
    screen.blit(player1, player1_rect)

    player2 = pygame.transform.scale(load_image('frog.png'), (200, 200))
    #start.add(player2)
    player2_rect = player2.get_rect(bottomleft=(((screen.get_width() - 200) // 3) * 2 - 225, 500))
    screen.blit(player2, player2_rect)

    player3 = pygame.transform.scale(load_image('enemy2.png'), (200, 200))
    #start.add(player3)
    player3_rect = player3.get_rect(bottomleft=(((screen.get_width() - 200) // 3) * 3 - 300, 500))
    screen.blit(player3, player3_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player1_rect.collidepoint(event.pos):
                    tile_images = {
                        'wall': pygame.transform.scale(load_image('block.png'),
                                                       (screen.get_width() // 31, screen.get_height() // 18)),
                        'portal': pygame.transform.scale(load_image('portal.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18)),
                        'empty': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'other': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'enemy3': pygame.transform.scale(load_image('player2.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18))
                    }
                elif player2_rect.collidepoint(event.pos):
                    tile_images = {
                        'wall': pygame.transform.scale(load_image('block.png'),
                                                       (screen.get_width() // 31, screen.get_height() // 18)),
                        'portal': pygame.transform.scale(load_image('portal.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18)),
                        'empty': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'other': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'enemy3': pygame.transform.scale(load_image('frog.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18))
                    }
                elif player3_rect.collidepoint(event.pos):
                    tile_images = {
                        'wall': pygame.transform.scale(load_image('block.png'),
                                                       (screen.get_width() // 31, screen.get_height() // 18)),
                        'portal': pygame.transform.scale(load_image('portal.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18)),
                        'empty': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'other': pygame.transform.scale(load_image('water22.jpg'),
                                                        (screen.get_width() // 31, screen.get_height() // 18)),
                        'enemy3': pygame.transform.scale(load_image('enemy2.png'),
                                                         (screen.get_width() // 31, screen.get_height() // 18))
                    }
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


#
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def winner_screen():
    intro_text = ['YOU WIN!!!!!!!!', '', 'OUR CONGRATULATIONS)))']

    fon = pygame.transform.scale(load_image('fon1.jpg'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    intro_text = ['GAME OVER', '', 'YOU LOOOSE HAHAHA']

    fon = pygame.transform.scale(load_image('black.png'), (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)



player_image = load_image('player1.png')
player_image = pygame.transform.scale(player_image, ((screen.get_width() // 31) // 5 * 4, (screen.get_height() // 18)
                                                     // 5 * 4))
pl_height, pl_width = (screen.get_width() // 31) // 5 * 4, (screen.get_height() // 18) // 5 * 4

tile_width, tile_height = screen.get_width() // 31, screen.get_height() // 18
# step = tile_height // 10
step = 10


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.x = pos_x * tile_width
        self.y = pos_y * tile_height
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.moves = 'l'

    def down(self):
        flag = 0
        global flag_level
        for i in range(self.image.get_width()):
            if (self.rect.y + step + tile_height) // tile_height < len(level_list) and (self.rect.x + i) // tile_width \
                    < len(level_list[0]) and level_list[(self.rect.y + step + tile_height) // tile_height][(self.rect.x
                                                                                                            + i) //
                                                                                                           tile_width] \
                    == "#":
                flag = 1
                self.rect.y += ((self.rect.y + step + tile_height) // tile_height) * tile_height - (self.rect.y +
                                                                                                    pl_height)
            elif (self.rect.y + step + tile_height) // tile_height < len(level_list) and (self.rect.x + i) // \
                    tile_width \
                    < len(level_list[0]) and level_list[(self.rect.y + step + tile_height) // tile_height][(self.rect.x
                                                                                                            + i) //
                                                                                                           tile_width] \
                    == "&":
                pygame.display.flip()
                clock.tick(FPS)
                flag_level = True
                return
        if self.rect.y + tile_height < tile_height * len(level_list) and flag == 0:
            self.rect.y += step
            self.y = self.rect.y

    def up(self):
        flag = 0
        global flag_level
        for i in range(self.image.get_width()):
            if level_list[(self.rect.y - step) // tile_height][(self.rect.x + i) // tile_width] == "#":
                flag = 1
                self.y -= self.rect.y - (((self.rect.y - step) // tile_height) * tile_height + tile_height)
            elif level_list[(self.rect.y - step) // tile_height][(self.rect.x + i) // tile_width] == "&":
                pygame.display.flip()
                clock.tick(FPS)
                flag_level = True
                return
        if self.rect.y > 0 and flag == 0:
            self.rect.y -= step
            self.y = self.rect.y

    def left(self):
        if self.moves == 'r':
            self.image = pygame.transform.flip(self.image, True, False)
        self.moves = 'l'
        flag = 0
        global flag_level
        for i in range(self.image.get_height()):
            if level_list[(self.rect.y + i) // tile_height][(self.rect.x - step) // tile_width] == "#":
                flag = 1
                self.rect.x -= self.rect.x - (((self.rect.x - step) // tile_width) * tile_width + tile_width)
            elif level_list[(self.rect.y + i) // tile_height][(self.rect.x - step) // tile_width] == "&":
                pygame.display.flip()
                clock.tick(FPS)
                flag_level = True
                return
        if self.rect.x > 0 and flag == 0:
            self.rect.x -= step
            self.x = self.rect.x

    def right(self):
        global flag_level
        if self.moves == 'l':
            self.image = pygame.transform.flip(self.image, True, False)
        self.moves = 'r'
        flag = 0
        for i in range(self.image.get_height()):
            if (self.rect.y + i) // tile_height < len(level_list) and (
                    self.rect.x + step + tile_width) // tile_width < len(level_list[0]) and \
                    level_list[(self.rect.y + i) // tile_height][
                        (self.rect.x + step + tile_width) // tile_width] == "#":
                flag = 1
                self.rect.x += ((self.rect.x + step + tile_width) // tile_width) * tile_width - (self.rect.x + pl_width)
            elif (self.rect.y + i) // tile_height < len(level_list) and (
                    self.rect.x + step + tile_width) // tile_width < len(level_list[0]) and \
                    level_list[(self.rect.y + i) // tile_height][
                        (self.rect.x + step + tile_width) // tile_width] == "&":
                pygame.display.flip()
                clock.tick(FPS)
                flag_level = True
                return
        if self.rect.x + tile_width < tile_width * len(level_list[0]) and flag == 0:
            self.rect.x += step
            self.x = self.rect.x

    def coords(self):
        return self.x, self.y


class Enemy(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('enemy2.png'), (50, 50))
    image2 = pygame.transform.scale(load_image('bomb_enemy.png'), (25, 25))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Enemy.image
        self.image2 = Enemy.image2
        self.rect = self.image.get_rect()
        self.x = x * tile_width
        self.y = y * tile_height
        self.attack_spisok = []
        # group[0].add(self)

    def cor(self):
        return self.x, self.y

    def update(self, player, *group):
        for i in enemy_group:
            # print(type(player.coords()[0]), type(i.cor()[0]))
            n = (((player.coords()[0] - i.cor()[0]) ** 2 + (player.coords()[1] - i.cor()[1]) ** 2) ** 0.5)
            if n <= 100:
                # if i not in self.attack_spisok:
                # self.attack_spisok.append(i)
                self.attack(i)
                # self.attack(self.attack_spisok, player.coords()[0] + tile_width // 2, player.coords()[1]
                # + tile_height // 2)

    def attack(self, elem):

        if len(hits) == 0:
            new_hit = Hit(elem, elem.cor()[0] + tile_width // 2, elem.cor()[1] + tile_height // 2,
                          player.coords()[0] + tile_width // 2, player.coords()[1] + tile_height // 2, 20)
            hits.add(new_hit)
        else:
            for i in hits:
                i.update()
                # clock1.tick(20)
            hits.draw(screen)
            # clock1.tick(20)


class Hit(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bomb_enemy.png'), (tile_width // 3, tile_height // 3))

    def __init__(self, elem, x, y, x_end, y_end, time, *group):
        super().__init__(*group)
        self.image = Hit.image
        # hits.add(self)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(x, y)
        self.x_end = x_end
        self.y_end = y_end
        self.time = time
        self.elem = elem
        self.step_x = abs(self.x - self.x_end) // self.time
        self.step_y = abs(self.y - self.y_end) // self.time
        self.n = 0

    def update(self):
        global hp
        self.n += 1
        # print(self.rect.x + tile_width // 2, self.x_end, self.rect.y + tile_height // 2, self.y_end)
        # print(pygame.sprite.spritecollide(player, hits, False))
        # print(self.rect.x + tile_width // 2 == self.x + self.step_x * self.time, self.rect.y + tile_height // 2 ==
        # self.step_y * self.time)

        # if not (self.rect.x + tile_width // 2 == self.x + self.step_x * self.time and self.rect.y + tile_height // 2
        # == self.step_y * self.time):
        if not self.n == self.time:
            if self.x > self.x_end:
                self.rect.x -= self.step_x
            else:
                self.rect.x += self.step_x
            if self.rect.y > self.y_end:
                self.rect.y -= self.step_y
            else:
                self.rect.y += self.step_y

        else:
            hp -= 50
            self.kill()


# основной персонаж


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
walls = pygame.sprite.Group()
portal = pygame.sprite.Group()
hits = pygame.sprite.Group()
enemies = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                tile = Tile('wall', x, y)
                walls.add(tile)
            elif level[y][x] == '*':
                Tile('other', x, y)
            elif level[y][x] == "%":
                Tile('empty', x, y)
                Tile('enemy3', x, y)
                enemy = Enemy(x, y, enemy_group)
                enemy_group.add(enemy)
                enemies.append(enemy)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                tile = Tile('portal', x, y)
                portal.add(tile)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


running = True
start_screen()
pygame.mixer.music.pause()
pygame.mixer.music.load("3level.mp3")
pygame.mixer.music.play(-1)
choose_character()
level_list = load_level('map2.txt')
# print("\n".join(level_list))
player, level_x, level_y = generate_level(level_list)
while running:
    all_sprites.draw(screen)
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # enemy_group.update(player, enemy_group)
    if key[pygame.K_DOWN]:
        player.down()
        enemy_group.update(player, enemy_group)
        # print(player.coords())
    if key[pygame.K_UP]:
        player.up()
        enemy_group.update(player, enemy_group)
        # print(player.coords())
    if key[pygame.K_LEFT]:
        player.left()
        enemy_group.update(player, enemy_group)
        # print(player.coords())
    if key[pygame.K_RIGHT]:
        player.right()
        enemy_group.update(player, enemy_group)
        # print(player.coords())
    player_group.draw(screen)
    clock.tick(20)
    pygame.display.flip()
    if flag_level is True:
        running = False
    if hp == 0:
        running = False

running = True
flag_level = False
if hp == 0:
    game_over()
    print('BOOO, LOOOOOSER')
    hp = 10000
    choose_character()
else:
    player_group.empty()
    all_sprites.empty()
    tiles_group.empty()
    enemy_group.empty()
    walls.empty()
    portal.empty()
    hits.empty()
    level_list = load_level('map3.txt')
    # print("\n".join(level_list))
    player, level_x, level_y = generate_level(level_list)
    while running:
        all_sprites.draw(screen)
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # enemy_group.update(player, enemy_group)
        if key[pygame.K_DOWN]:
            player.down()
            enemy_group.update(player, enemy_group)
            # print(player.coords())
        if key[pygame.K_UP]:
            player.up()
            enemy_group.update(player, enemy_group)
            # print(player.coords())
        if key[pygame.K_LEFT]:
            player.left()
            enemy_group.update(player, enemy_group)
            # print(player.coords())
        if key[pygame.K_RIGHT]:
            player.right()
            enemy_group.update(player, enemy_group)
            # print(player.coords())
        player_group.draw(screen)
        clock.tick(20)
        pygame.display.flip()
        if flag_level is True:
            running = False
        if hp == 0:
            running = False
    if hp == 0:
        game_over()
        print('BOOOOO, LOOOSER')
        hp = 10000
        choose_character()
    else:
        winner_screen()
        print('YOU ARE A WINNER')
        hp = 10000
        choose_character()
    pygame.mixer.music.pause()
    pygame.quit()
