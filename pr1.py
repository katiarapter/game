import pygame
import os
import sys

FPS = 50
clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('MARIOOOO')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('player.png')
player_image = pygame.transform.scale(player_image, (45, 45))

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def init(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().init(tiles_group, all_sprites, boxes_group)
        else:
            super().init(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def init(self, pos_x, pos_y):
        super().init(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_(self, coords):
        self.rect = self.rect.move(coords[0], coords[1])
        if pygame.sprite.spritecollideany(self, boxes_group):
            self.rect = self.rect.move(-coords[0], -coords[1])


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
boxes = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                boxes.append((x * 50 + 50, y * 50 + 50))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player, level_x, level_y = generate_level(load_level('map.txt'))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
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
            if event.type == pygame.KEYDOWN:
                all_sprites.draw(screen)
                if event.key == pygame.K_DOWN:
                    player.update_([0, 50])
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                if event.key == pygame.K_UP:
                    player.update_([0, -50])
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                if event.key == pygame.K_LEFT:
                    player.update_([-50, 0])
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                if event.key == pygame.K_RIGHT:
                    player.update_([50, 0])
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
