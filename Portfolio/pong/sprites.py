from settings import *
import pygame as pg

class Ball(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(WHITE)
        self.rect = self.image.get_rect()