import pygame as pg
from pygame.locals import *
from settings import *
import random
import time
import threading

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = PLAYER_IMAGE
		self.image.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.image.get_rect()
		self.pos = vec(WIDTH/2, HEIGHT/2)
		self.rect.center = self.pos
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.bombs = 5
		self.maxLives = 5
		self.lives = self.maxLives
		self.enemiesHit = 0

	def update(self):
		if self.lives > self.maxLives:
			self.lives = self.maxLives
		self.acc = vec(0,0)
		#keys = pg.key.get_pressed()
		"""#             DONT USE BECAUSE OF LAG
		if keys[pg.K_a]:
			self.acc.x = -PLAYER_SPEED
		if keys[pg.K_d]:
			self.acc.x = PLAYER_SPEED
		if keys[pg.K_w]:
			self.acc.y = -PLAYER_SPEED
		if keys[pg.K_s]:
			self.acc.y = PLAYER_SPEED
		"""

		self.acc += self.vel * -PLAYER_FRICTION
		self.vel += self.acc
		#self.pos += self.vel + 0.5 * self.acc
		#self.pos.x = pg.mouse.get_pos()[0]
		#self.pos.y = pg.mouse.get_pos()[1
		self.pos = vec(pg.mouse.get_pos())

		if self.pos.x > WIDTH:
			self.pos.x = WIDTH
		if self.pos.x < 0:
			self.pos.x = 0
		if self.pos.y > HEIGHT:
			self.pos.y = HEIGHT
		if self.pos.y < 0:
			self.pos.y = 0
		self.rect.center = self.pos
	def damage(self, amount):
		self.lives -= amount
	
	def reset(self):
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.pos = vec(WIDTH/2, HEIGHT/2)
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.bombs = 5
		self.lives = 5
		self.enemiesHit = 0
	
player = Player()

class deathHeart(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = DHEARTIMAGE
		self.image.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.image.get_rect()
		self.pos = vec(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10))
		self.rect.center = self.pos
		self.damage = 0.5
		self.timeAlive = 0
		self.distance = vec.distance_to(self.pos, player.pos)
		if pg.sprite.collide_rect(self, player):
			self.kill()
			
		t2 = threading.Thread(target=self.spawn).start()

	
	def attack(self):
		player.damage(0.5)
	
	
	def update(self):
		self.timeAlive += 1
	
	def spawn(self):
		time.sleep(random.randint(3,5))
		self.kill()

class deathLeft(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = DLEFTIMAGE
		self.image.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.image.get_rect()
		self.pos = vec(WIDTH, player.pos.y)
		self.rect.center = self.pos
		self.damage = 1
		self.timeAlive = 0
		deathMove = threading.Thread(target=self.spawn).start()
	

	def attack(self):
		player.damage(1)
	
	
	
	def update(self):
		self.timeAlive += 1
	
		
	def spawn(self):
		while self.pos.x > -10:
			self.pos.x -= 10
			self.rect.center = self.pos
			time.sleep(0.01)
		self.kill()

class deathRight(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = DRIGHTIMAGE
		self.image.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.image.get_rect()
		self.pos = vec(0, player.pos.y)
		self.rect.center = self.pos
		self.damage = 1
		self.timeAlive = 0
		deathMove = threading.Thread(target=self.spawn).start()
	
	def attack(self):
		player.damage(1)
	
	
	def update(self):
		self.timeAlive += 1

	def spawn(self):
		while self.pos.x < WIDTH+10:
			self.pos.x += 10
			self.rect.center = self.pos
			time.sleep(0.01)
		self.kill()

class healthHeart(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = HHEARTIMAGE
		self.image.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.image.get_rect()
		self.pos = vec(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10))
		self.rect.center = self.pos
		self.damage = -1
		self.timeAlive = 0
		if player.lives <= player.maxLives:
			self.kill()
		t2 = threading.Thread(target=self.spawn).start()
	
	def attack(self):
		player.lives += 0.5
	
	def update(self):
		self.timeAlive += 1
	
	def spawn(self):
		time.sleep(random.randint(2,4))
		self.kill()

enemies = [deathHeart, deathLeft, deathRight]