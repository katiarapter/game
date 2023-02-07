import pygame
import sys
import os


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
