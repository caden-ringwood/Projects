# tile game
# caden ringwood
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

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "imgs")
        map_folder = path.join(game_folder, "maps")
        hitman_folder = path.join(img_folder, "Hitman 1")
        manBlue_folder = path.join(img_folder, "Man Blue")
        manBrown_folder = path.join(img_folder, "Man Brown")
        manOld_folder = path.join(img_folder, "Man Old")
        robot_folder = path.join(img_folder, "Robot 1")
        soldier_folder = path.join(img_folder, "Soldier 1")
        survivor_folder = path.join(img_folder, "Survivor 1")
        tiles_folder = path.join(img_folder, "Tiles")
        woman_folder = path.join(img_folder, "Woman Green")
        zombies_folder = path.join(img_folder, "Zombie 1")
        effects_folder = path.join(img_folder, "visual effects")
        sounds_folder = path.join(game_folder, "sounds")
        music_folder = path.join(sounds_folder, "music")
        pain_folder = path.join(sounds_folder, "music")


        self.map = Tiled_Map(path.join(map_folder, "map_1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(survivor_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(zombies_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(tiles_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (30, 30))
        self.wall_img = pg.image.load(path.join(tiles_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(effects_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
            print(item)
        # sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(sounds_folder, EFFECTS_SOUNDS[type]))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, col, row)
        #         if tile == "P":
        #             self.player = Player(self, col, row)
        #         if tile == "M":
        #             self.mob = Mob(self, col, row)
        for tile_obj in self.map.tmxdata.objects:
            obj_center = vec(tile_obj.x + tile_obj.width / 2, tile_obj.y + tile_obj.height / 2)
            if tile_obj.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_obj.name == "mob":
                Mob(self, obj_center.x, obj_center.y)
            if tile_obj.name == "wall":
                Obstical(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
            if tile_obj.name in ["health"]:
                Item(self, obj_center, tile_obj.name)
        self.camera = Camera(self.map.width, self.map.height) 
        self.draw_debug = False
        # self.effects_sounds["level_start"].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
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
        # player hists items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds["health_up"].play()
                self.player.add_health(HEATH_PACK_AMOUNT)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullet hits mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_heath()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(sprite.hit_rect), 1)
                for wall in self.walls:
                    pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, RED, self.player.hit_rect, 3)
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
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
