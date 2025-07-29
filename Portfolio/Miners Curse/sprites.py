import random
import pygame as pg
from settings import *
from tile_map import collide_hit_rect
vec = pg.math.Vector2

from os import path
import pygame as pg
import sys
from settings import *
from sprites import *
from tile_map import *
import random


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.through_rect = PLAYER_THROUGH_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_update = 0
        self.facing = "R"
        self.health = PLAYER_HEALTH
        self.weapons = ["pick", "shovel", "tnt"]

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.facing = "L"
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.facing = "R"
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.facing = "U"
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.facing = "D"
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > ATTACK_SPEED:
            for weapon in self.weapons:
                if weapon == "pick":
                    PickAxe(self.game, self.pos)
                elif weapon == "shovel":
                    Shovel(self.game, self.pos)
                elif weapon == "tnt":
                    x = random.randrange(0, WIDTH)
                    y = random.randrange(0, HEIGHT)
                    target = vec(x, y)
                    rot = (target - self.pos).angle_to(vec(1, 0))
                    dir = vec(1, 0).rotate(-rot)
                    Tnt(self.game, dir, self.pos)
                self.last_update = now
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.through_rect.center = self.rect.center

class PickAxe(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = ATTACK_LAYER
        self.groups = game.all_sprites, game.attacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.pick_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.facing = self.game.player.facing
        if self.facing == "R":
            self.pos -= vec(TILESIZE - 5, 0)
        elif self.facing == "L":
            self.image = pg.transform.flip(self.image.copy(), True, False)
            self.pos -= vec(-TILESIZE, 0)
        elif self.facing == "U":
            self.image = pg.transform.rotate(self.image.copy(), 90)
            self.pos -= vec(+9, -TILESIZE - 13)
        elif self.facing == "D":
            self.image = pg.transform.rotate(self.image.copy(), -90)
            self.pos -= vec(10, TILESIZE - 2)
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.game.player.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > ATTACK_DIR:
            self.kill()

class Shovel(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = ATTACK_LAYER
        self.groups = game.all_sprites, game.attacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shovel_img
        self.image = pg.transform.scale(self.image, (45, 11))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.facing = self.game.player.facing
        if self.facing == "R":
            self.pos -= vec(-TILESIZE, 0)
        elif self.facing == "L":
            self.image = pg.transform.flip(self.image.copy(), True, False)
            self.pos -= vec(TILESIZE, 0)
        elif self.facing == "U":
            self.image = pg.transform.rotate(self.image.copy(), 90)
            self.pos -= vec(0 - 17, TILESIZE + 25)
        elif self.facing == "D":
            self.image = pg.transform.rotate(self.image.copy(), -90)
            self.pos -= vec(0 - 18, -TILESIZE + 10)
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.game.player.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > ATTACK_DIR:
            self.kill()

class Tnt(pg.sprite.Sprite):
    def __init__(self, game, dir, pos):
        self._layer = ATTACK_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.tnt_img
        self.image = pg.transform.scale(self.image, (20, 15))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = self.pos
        self.vel = dir * THROUGH_SPEED * random.uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += vec(self.vel * self.game.dt)
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > THROUGH_TIME:
            Explotion(self.game, self.pos)
            self.kill()

class Explotion(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = ATTACK_LAYER
        self.groups = game.all_sprites, game.attacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.epl_img
        self.image = pg.transform.scale(self.image, (90, 90))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > ATTACK_DIR:
            self.kill()

class Rat(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.mobs, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.rat_img
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = RAT_HEALTH


    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(RAT_SPEED)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.kills += 1
            print(self.game.kills)
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstical(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
