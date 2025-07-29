import pygame as pg
from settings import *
from tile_map import collide_hit_rect
import random
vec = pg.math.Vector2

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
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pollen = 0
        self.score = 0

        self.pos = 0

        self.game.bee_snd.play(-1)


    def update(self):
        # move with mouse
        mousex, mousey = pg.mouse.get_pos()
        self.pos = vec(mousex, mousey)

        self.max_pollen = len(self.game.bees) * BEE_CARRY
        if self.pollen > self.max_pollen:
            self.pollen = self.max_pollen

        if len(self.game.bees) < 1:
            self.game.bee_snd.stop

class Bee(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bees
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.right_img = game.bee_img
        self.left_img = pg.transform.flip(self.right_img.copy(), True, False)
        self.image = self.right_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect
        self.hit_rect.centerx = self.rect.centerx
        self.hit_rect.centery = self.rect.centery
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = BEE_HEALTH
        self.speed = BEE_SPEED


    def avoid_mobs(self):
        for bee in self.game.bees:
            if bee != self:
                dist = self.pos - bee.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        if self.vel.x < 0:
            self.image = self.left_img
            self.image.set_colorkey(WHITE)
        else:
            self.image = self.right_img
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

class Queen(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.queens, game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.health = QUEEN_HEALTH
        self.pos = self.rect.center

class Hive(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.hives, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.health = NEW_BEE

    def new_bee(self):
        self.health = NEW_BEE
        x = random.randint(self.rect.left, self.rect.right)
        y = random.randint(self.rect.top, self.rect.bottom)
        Bee(self.game, x, y)
        self.game.queen.health += 15
        if self.game.queen.health > QUEEN_HEALTH:
            self.game.queen.health = QUEEN_HEALTH
        self.game.player.score += 40

class Flower(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.flowers, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Wasp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wasps
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.right_img = game.wasp_img
        self.right_img = pg.transform.scale(self.right_img, (35, 40))
        self.left_img = pg.transform.flip(self.right_img.copy(), True, False)
        self.image = self.right_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = WASP_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = WASP_HEALTH
        self.speed = random.choice(WASP_SPEED)

        self.game.wasp_snd.play(-1)

    def avoid_mobs(self):
        for wasp in self.game.wasps:
            if wasp != self:
                dist = self.pos - wasp.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.queen.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        if self.acc.x == 0:
            self.acc.x = 1
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        if self.vel.x < 0:
            self.image = self.left_img
            self.image.set_colorkey(WHITE)
        else:
            self.image = self.right_img
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.player.score += 100
            self.game.squish_snd.play()
            self.kill()

        if len(self.game.wasps) == 0:
            self.game.wasp_snd.stop()

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
