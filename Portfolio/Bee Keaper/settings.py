import pygame as pg

# define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 155, 50)
PINK = (155, 66, 77)
HONEY = (235, 169, 55)
# sounds
BGMUSIC = ["jingles_HIT00.ogg", "jingles_HIT01.ogg", "jingles_HIT02.ogg", "jingles_HIT03.ogg", "jingles_HIT04.ogg",
           "jingles_HIT05.ogg", "jingles_HIT06.ogg", "jingles_HIT07.ogg", "jingles_HIT08.ogg", "jingles_HIT09.ogg",
           "jingles_HIT10.ogg", "jingles_HIT11.ogg", "jingles_HIT12.ogg", "jingles_HIT13.ogg", "jingles_HIT14.ogg",
           "jingles_HIT15.ogg", "jingles_HIT16.ogg"]

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Bee Keeper"
HS_FILE = "highscore.txt"
BGCOLOR = DARKGREY

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# sprite settings
AVOID_RADIUS = 15
# queen
QUEEN_HEALTH = 100
# bees
BEE_SPEED = 90
BEE_HIT_RECT = pg.Rect(0, 0, 15, 11)
BEE_HEALTH = 30
BEE_CARRY = 10
NEW_BEE = 20
HARVEST = 2
FLOWER_RATE = 500
BEE_DAMAGE = 10
# wasps
WASP_HEALTH = 20
WASP_SPEED = [40, 30, 50]
WASP_HIT_RECT = pg.Rect(0, 0, 15, 24)
WASP_DAMAGE = 10
ATTACK_SPEED = 850
FIRST_WAVE = 20000
