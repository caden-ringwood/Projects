# tile game
# caden ringwood
import random
from os import path
import pygame as pg
import sys
from settings import *
from sprites import *
from tile_map import *

# hud functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

font_name = pg.font.match_font("Comic Sands MS")
def draw_text(surf, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.last_update = 0
        self.kills = 0

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, "imgs")
        self.map_folder = path.join(game_folder, "maps")
        self.map = Tiled_Map(path.join(self.map_folder, "map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(self.img_folder, "player.png")).convert_alpha()
        self.rat_img = pg.image.load(path.join(self.img_folder, "rat.png")).convert_alpha()
        self.tnt_img = pg.image.load(path.join(self.img_folder, "tnt.png")).convert_alpha()
        self.epl_img = pg.image.load(path.join(self.img_folder, "explo.png")).convert_alpha()
        self.shovel_img = pg.image.load(path.join(self.img_folder, "shovel.png")).convert_alpha()
        self.pick_img = pg.image.load(path.join(self.img_folder, "pick.png")).convert_alpha()
        self.title_font = path.join(self.img_folder, "ZOMBIE.TTF")

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        for tile_obj in self.map.tmxdata.objects:
            obj_center = vec(tile_obj.x + tile_obj.width / 2, tile_obj.y + tile_obj.height / 2)
            if tile_obj.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_obj.name == "wall":
                Obstical(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
        self.player = Player(self, 5, 5)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # hit mob
        hits = pg.sprite.groupcollide(self.mobs, self.attacks, False, False)
        for hit in hits:
            hit.health -= ATTACK_DAMAGE
            hit.vel = hit.vel * -2.5
        # mob hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            now = pg.time.get_ticks()
            if now - self.last_update > HIT_DIR:
                self.last_update = now
                self.player.health -= MOB_DAMAGE
                hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if len(self.mobs) <= 3:
            for i in range(10):
                print("mob")
                col = random.randrange(TILESIZE * 2, (WIDTH - TILESIZE))
                row = random.randrange(TILESIZE * 2, (HEIGHT - TILESIZE))
                self.rat = Rat(self, col, row)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        self.start = True
        play = False
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, TITLE, 120, RED, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "WASD or arrows to move.", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen,
                  "You will attack automatically",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
        draw_text(self.screen,
                  "Your health is on the top of the screen.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        draw_text(self.screen,
                  "Kill the rats to gain points.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 60)
        draw_text(self.screen, "Press a key to play", 30, GREEN, WIDTH / 2, HEIGHT * 7 / 8)
        pg.display.flip()
        self.wait_for_key()
        return True

    def show_GameOver_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Press a key to play again", self.title_font, 75, WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_GameOver_screen()
