import pygame as pg
vec = pg.math.Vector2

# define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (100, 55, 0)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Game Title"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = "tile_96.png"

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = "survivor1_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# weapon settings
BULLET_IMG = "bullet.png"
WEAPONS = {}
WEAPONS["pistol"] = {"bullet_speed": 500,
                     "bullet_lifetime": 1000,
                     "rate": 250,
                     "kickback": 200,
                     "spread": 5,
                     "damage": 10,
                     "bullet_size": "lg",
                     "bullet_count": 1}
WEAPONS["shotgun"] = {"bullet_speed": 400,
                     "bullet_lifetime": 500,
                     "rate": 1000,
                     "kickback": 300,
                     "spread": 20,
                     "damage": 5,
                     "bullet_size": "sm",
                     "bullet_count": 12}
BULLET_OFFSET = vec(25, 10)


# mob settings
MOB_HEALTH = 100
MOB_IMG = "zoimbie1_hold.png"
SPLAT = "splat green.png"
MOB_SPEEDS = [75, 100, 175, 150, 150, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 65
DETECT_RADIUS = 400

# Effects
MUZZLE_FLASHES = ["smoke_01.png", "smoke_02.png", "smoke_03.png", "smoke_04.png", "smoke_05.png", "smoke_06.png",
                  "smoke_07.png", "smoke_08.png", "smoke_09.png", "smoke_10.png"]
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 40)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"

# Layers
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4

# Items
ITEM_IMAGES = {"health": "health_pack.png",
               "shotgun": "obj_shotgun.png"}
HEATH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.2

# sounds
BG_MUSIC = "espionage.ogg"
PLAYER_HIT_SOUNDS = ["pain/8.wav", "pain/10.wav", "pain/11.wav", "pain/9.wav", "pain/11.wav"]
ZOMBIE_MOAN_SOUNDS = ["snd_brains2.wav", "snd_brains3.wav", "snd_zombie-roar-1.wav", "snd_zombie-roar-2.wav", "snd_zombie-roar-3.wav",
                      "snd_zombie-roar-4.wav", "snd_zombie-roar-5.wav", "snd_zombie-roar-6.wav", "snd_zombie-roar-7.wav", "snd_zombie-roar-8.wav"]
ZOMBIE_HIT_SOUND = ["snd_splat-15.wav"]
WEAPON_SOUNDS = {"pistol": ["pistol.wav"],
                 "shotgun": ["shotgun.wav"]}
EFFECTS_SOUNDS = {'level_start': 'snd_level_start.wav',
                  'health_up': 'snd_health_pack.wav',
                  "gun_pickup": "gun_pickup.wav"}

