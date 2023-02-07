import pygame
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
# screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

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


#
tile_images = {
    'wall': pygame.transform.scale(load_image('block.png'), (50, 50)),
    'empty': pygame.transform.scale(load_image('grass.png'), (50, 50)),
    'other': pygame.transform.scale(load_image('out.png'), (50, 50)),
    'enemy2': pygame.transform.scale(load_image('enemy1.png'), (50, 50)),
    'enemy1': pygame.transform.scale(load_image('enemy2.png'), (50, 50)),
    'enemy3': pygame.transform.scale(load_image('enemy3.gif'), (50, 50))
}
player_image = load_image('player1.png')
player_image = pygame.transform.scale(player_image, (40, 40))

tile_width = tile_height = 50


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
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.moves = 'l'

    def down(self):
        if self.rect.y + 50 < screen.get_height() and level_list[(self.rect.y + 60) // 50][self.rect.x // 50] != "#":
            self.rect.y += 10

    def up(self):
        if self.rect.y > 0 and level_list[(self.rect.y - 10) // 50][self.rect.x // 50] != "#":
            self.rect.y -= 10

    def left(self):
        if self.moves == 'r':
            self.image = pygame.transform.flip(self.image, True, False)
        self.moves = 'l'
        flag = 0
        for i in range(self.image.get_height()):
            if level_list[(self.rect.y + i) // 50][(self.rect.x - 10) // 50] == "#":
                flag = 1
        if self.rect.x > 0 and flag == 0:
            self.rect.x -= 10

    def right(self):
        if self.moves == 'l':
            self.image = pygame.transform.flip(self.image, True, False)
        self.moves = 'r'
        flag = 0
        for i in range(self.image.get_height()):
            if level_list[(self.rect.y + i) // 50][(self.rect.x + 60) // 50] == "#":
                flag = 1
        if self.rect.x + 50 < screen.get_width() and flag == 0:
            self.rect.x += 10


#
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls = pygame.sprite.Group()


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
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


running = True
start_screen()
level_list = load_level('map4.txt')
print("\n".join(level_list))
player, level_x, level_y = generate_level(level_list)
while running:
    all_sprites.draw(screen)
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if key[pygame.K_DOWN]:
        player.down()
    if key[pygame.K_UP]:
        player.up()
    if key[pygame.K_LEFT]:
        player.left()
    if key[pygame.K_RIGHT]:
        player.right()
    player_group.draw(screen)
    clock.tick(20)
    pygame.display.flip()
pygame.quit()
