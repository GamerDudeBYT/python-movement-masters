try:
	from screeninfo import get_monitors
except:
	print("Could not find screeninfo module. Install it with 'pip install screeninfo'")
	quit()

import pygame as pg

for monitor in get_monitors():
    if monitor.is_primary:
        WIDTH = monitor.width
        HEIGHT = monitor.height

TITLE = "Movement Masters Beta Test"
DESCRIPTION = "The goal of this game is to survive for as long as you can and dodge all of the attacks thrown at you. Every time you respawn, the game gets harder."
DESCRIPTION2 = "Green enemies hurt you. Blue enemies heal you. Your bombs don't regenerate so you need to reserve them."
FPS = 60
FONT_NAME = "arial"
HS_FILE = "bestTime.txt"
ICONIMAGE = pg.image.load('images/newLogo.png')

PLAYER_SPEED = 2
PLAYER_FRICTION = 0.12
PLAYER_KILLZONE = 300

WHITE = "#ffffff"
RED = "#FF0000"

TITLECOLOUR = "#2ad1ce"
BACKGROUND = "#5c5752"

SMALLMODE = True

if SMALLMODE == True:
	TEXTDIFFERENCE = 10
	PLAYER_IMAGE = pg.image.load("images/pixelHeart3Small.png")
	DHEARTIMAGE = pg.image.load("images/deathHeartSmall.png")
	DLEFTIMAGE = pg.image.load("images/deathLeftSmall.png")
	DRIGHTIMAGE = pg.image.load("images/deathRightSmall.png")
	HHEARTIMAGE = pg.image.load("images/healthHeartSmall.png")
else:
	TEXTDIFFERENCE = 0
	PLAYER_IMAGE = pg.image.load("images/pixelHeart3.png")
	DHEARTIMAGE = pg.image.load("images/deathHeart.png")
	DLEFTIMAGE = pg.image.load("images/deathLeft.png")
	DRIGHTIMAGE = pg.image.load("images/deathRight.png")
	HHEARTIMAGE = pg.image.load("images/healthHeart.png")


