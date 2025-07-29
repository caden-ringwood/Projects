# Bee game
# caden ringwood
from os import path
import pygame as pg
import sys
from settings import *
from sprites import *
from tile_map import *
import random

def draw_bar(surf, x, y, pct, dir="h", fillcolor=GREEN, div=100, len = 100):
    if pct < 0:
        pct = 0
    if dir == "h":
        bar_length = len
        bar_height = 10
        fill = (pct / div) * bar_length
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        fill_rect = pg.Rect(x, y, fill, bar_height)
    if dir == "v":
        bar_length = 15
        bar_height = 150
        fill = (pct / div) * bar_height
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        fill_rect = pg.Rect(x, y, bar_length, fill)
    pg.draw.rect(surf, fillcolor, fill_rect)
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
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.last_flower = 0
        self.last_hit = 0
        self.last_wave = 0
        self.wave_speed = FIRST_WAVE
        self.start = True

    def load_data(self):
        # define folders
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "imgs")
        tile_folder = path.join(img_folder, "tile sheets")
        audio_folder = path.join(game_folder, "audio")
        sounds_folder = path.join(audio_folder, "sound efects")

        # load in map
        self.map = Tiled_Map(path.join(tile_folder, "beeMap.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # load in imgs
        self.bee_img = pg.image.load(path.join(img_folder, "bee.png")).convert_alpha()
        self.wasp_img = pg.image.load(path.join(img_folder, "wasp.png")).convert_alpha()

        # load snds
        pg.mixer.music.load(path.join(audio_folder, "bee song.mp3"))
        self.bee_snd = pg.mixer.Sound(path.join(sounds_folder, "bee01.wav"))
        self.wasp_snd = pg.mixer.Sound(path.join(sounds_folder, "wasp.wav"))
        self.die_snd = pg.mixer.Sound(path.join(sounds_folder, "die.wav"))
        self.squish_snd = pg.mixer.Sound(path.join(sounds_folder, "squish.wav"))
        self.hit_snd = pg.mixer.Sound(path.join(sounds_folder, "hit.wav"))

        # load high score
        self.dir = game_folder
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.bees = pg.sprite.Group()
        self.wasps = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.hives = pg.sprite.Group()
        self.flowers = pg.sprite.Group()
        self.queens = pg.sprite.Group()
        self.player = Player(self)
        for tile_obj in self.map.tmxdata.objects:
            obj_center = vec(tile_obj.x + tile_obj.width / 2, tile_obj.y + tile_obj.height / 2)
            if tile_obj.name == "hive":
                self.hive = Hive(self, obj_center.x, obj_center.y, tile_obj.width, tile_obj.height)
            if tile_obj.name == "wall":
                Obstical(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
            if tile_obj.name == "flowers":
                Flower(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
            if tile_obj.name == "queen":
                self.queen = Queen(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
        x = random.randint(self.hive.rect.left, self.hive.rect.right)
        y = random.randint(self.hive.rect.top, self.hive.rect.bottom)
        self.main_bee = Bee(self, x, y)
        for i in range(7):
            x = random.randint(self.hive.rect.left, self.hive.rect.right)
            y = random.randint(self.hive.rect.top, self.hive.rect.bottom)
            Bee(self, x, y)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            if self.start:
                now = pg.time.get_ticks()
                self.last_wave = now
            self.start = False
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

        # wasp waves
        now = pg.time.get_ticks()
        if now - self.last_wave > self.wave_speed:
            num = [1, 1, 1, 2, 2, 2, 2, 3]
            w = random.choice(num)
            for i in range(w):
                let = ["l", "r", "b"]
                side = random.choice(let)
                if side == "l":
                    x = random.randint(25, 40)
                    y = random.randint(25, HEIGHT - 25)
                if side == "r":
                    x = random.randint(WIDTH - 40, WIDTH - 25)
                    y = random.randint(25, HEIGHT - 25)
                if side == "b":
                    x = random.randint(25, WIDTH - 25)
                    y = random.randint(HEIGHT - 40, HEIGHT - 25)
                Wasp(self, x, y)
            self.last_wave = now
            self.wave_speed = random.randint(15000, 40000)

        # collitions
        # bees by flowers
        hits = pg.sprite.groupcollide(self.bees, self.flowers, False, False)
        for bee in hits:
            now = pg.time.get_ticks()
            if now - self.last_flower > FLOWER_RATE:
                self.player.pollen += HARVEST
                self.player.score += 1
                if self.player.pollen > self.player.max_pollen:
                    self.player.pollen = self.player.max_pollen
                self.last_flower = now
        # bees by hive
        hits = pg.sprite.groupcollide(self.bees, self.hives, False, False)
        if self.player.pollen > 0 and hits:
            for i in range(self.player.pollen):
                self.hive.health -= 1
                self.player.pollen -= 1
                if self.hive.health <= 0:
                    self.hive.health = NEW_BEE
                    self.hive.new_bee()
        # bee hit wasp
        hits = pg.sprite.groupcollide(self.wasps, self.bees, False, True)
        for wasp in hits:
            for bee in hits[wasp]:
                wasp.health -= BEE_DAMAGE
                self.die_snd.play()
            wasp.vel = vec(0, 0)
        # wasp hit queen
        hits = pg.sprite.groupcollide(self.wasps, self.queens, False, False)
        for wasp in hits:
            now = pg.time.get_ticks()
            if now - self.last_hit > ATTACK_SPEED:
                self.queen.health -= WASP_DAMAGE
                self.hit_snd.play()
                self.last_hit = now
        # queen dies or no bees
        if self.queen.health <= 0 or len(self.bees) == 0:
            self.playing = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, (0, 0))
        for sprite in self.all_sprites:
            try:
                self.screen.blit(sprite.image, (sprite.rect.centerx, sprite.rect.centery))
            except:
                pass
        draw_bar(self.screen, WIDTH / 2 - 150, HEIGHT - 28, self.player.pollen, "h", HONEY, self.player.max_pollen, len=300)
        draw_bar(self.screen, WIDTH / 2 - 50, 36, self.queen.health, "h", RED)
        draw_text(self.screen, str(self.player.pollen), 20, WHITE, WIDTH / 2, HEIGHT - 40)
        draw_text(self.screen, str(self.player.score), 40, BLACK, WIDTH / 2, 100)
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
        draw_text(self.screen, TITLE, 120, HONEY, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "The bees will follow your mouse.", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen,
                  "Lead the bees to the flowers to gather pollen.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
        draw_text(self.screen,
                  "The bar at the bottom of the screen displays the amount of pollen you have.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        draw_text(self.screen,
                  "Take the pollen back to the hive to get more bees and heal the hive.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 60)
        draw_text(self.screen,
                  "It costs 20 pollen for a new bee, but the more bees the more pollen you can carry.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
        draw_text(self.screen,
                  "Watch out! Wasps will try to attack the hive, and it takes two bees to kill one wasp.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 100)
        draw_text(self.screen,
                  "If your hive dies or you run out of bees you lose.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 120)
        draw_text(self.screen,
                  "Gain points by getting pollen, more bees, and killing wasps.",
                  30, WHITE, WIDTH / 2, HEIGHT / 2 + 140)
        draw_text(self.screen, "Press a key to play", 30, GREEN, WIDTH / 2, HEIGHT * 7 / 8)
        draw_text(self.screen, "High Score: " + str(self.highscore), 40, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        return True

    def show_go_screen(self):
        self.start = True
        pg.mixer.music.stop()
        self.wasp_snd.stop()
        self.bee_snd.stop()
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, "GAME OVER", 120, RED, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Score: " + str(self.player.score), 40, HONEY, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to play again", 40, GREEN, WIDTH / 2, HEIGHT * 7 / 8)
        if self.player.score > self.highscore:
            self.highscore = self.player.score
            draw_text(self.screen, "NEW HIGH SCORE!", 40, GREEN, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.player.score))
        else:
            draw_text(self.screen, "High Score: " + str(self.highscore), 40, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
play = g.show_start_screen()
while play:
    g.new()
    g.run()
    g.show_go_screen()
