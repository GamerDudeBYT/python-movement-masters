#These 3 are part of python
import time
import threading
import random

try: # Try to import pygame
	import pygame as pg
except:
	print("Pygame was not found. Use 'pip install pygame' to install it.")
	quit()
try: # Try to import the sprites and settings files
	from settings import *
	import sprites
except:
	print("settings.py or sprites.py not found. Have you got settings.py and sprites.py in the same directory as this file?")
	quit()

class Game:
	def __init__(self): # Initialise Pygame, set up the window, clock, font and highscore
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
		pg.display.set_caption(TITLE)
		pg.display.set_icon(ICONIMAGE)
		self.clock = pg.time.Clock()
		self.running = True
		self.font_name = pg.font.match_font(FONT_NAME)
		self.loadData()

	def new(self): # Reset the game
		self.developer = False
		self.hardMode = False
		self.timeAlive = 0
		self.allSprites = pg.sprite.Group()
		self.enemySprites = pg.sprite.Group()
		self.player = sprites.player
		self.player.reset()
		self.allSprites.add(self.player)
		self.currentTime = 0
		self.lastTime = time.time()
		self.startTime = pg.time.get_ticks()
		self.timing = True
		self.spawning = True
		self.wipeEnemies()
		self.run()

	def run(self): # Game loop and enemy spawner thread
		self.playing = True
		self.t1 = threading.Thread(target=self.enemySpawner).start()
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.gameScreen()
			self.timer()

	def loadData(self): # Get highscore from bestTime.txt
		with open(HS_FILE, "r") as f:
			try:
				self.highscore = float(f.read())
			except:
				self.highscore = 0
				print("Couldn't use highscore. Defaulting to 0")

	def enemySpawner(self): # Threaded along with rest of code to handle enemies. Made to work with reset makes game harder feature.
		time.sleep(3)
		while True:
			if self.hardMode == True:
				for i in range(3):
					for i in range(3):
						if self.playing == False:
							break
						if self.spawning == False:
							self.wipeEnemies()
							continue
						enemyChoice = random.choice(sprites.enemies)
						if enemyChoice == sprites.deathHeart:
							continue
						newEnemy = enemyChoice()
						self.allSprites.add(newEnemy)
						self.enemySprites.add(newEnemy)
						time.sleep(random.uniform(1,1.5))
						self.heartSpread()
			else:
				for i in range(3):
					if self.playing == False:
						break
					if self.spawning == False:
						self.wipeEnemies()
						continue
					enemyChoice = random.choice(sprites.enemies)
					if enemyChoice == sprites.deathHeart:
						continue
					newEnemy = enemyChoice()
					self.allSprites.add(newEnemy)
					self.enemySprites.add(newEnemy)
					time.sleep(random.uniform(1,1.5))
			self.heartSpread()
			time.sleep(2)

	def heartSpread(self): # Spawn a group of death hearts. Happens every wave of enemies.
		if self.spawning == False:
			self.wipeEnemies()
		heartNumber = random.randint(4,9)
		for i in range(heartNumber):
			newDeathHeart = sprites.deathHeart()
			self.allSprites.add(newDeathHeart)
			self.enemySprites.add(newDeathHeart)
		newHealthHeart = sprites.healthHeart()
		self.allSprites.add(newHealthHeart)
		self.enemySprites.add(newHealthHeart)

	def wipeEnemies(self): # Kill all the enemies. Used for bombs and reset
		for enemy in self.enemySprites:
			enemy.kill()

	def update(self): # Update all sprites - Positions and other things.
		self.allSprites.update()

	def events(self): # Pygame events and player collisions.
		for event in pg.event.get(): # Pygame
			if event.type == pg.QUIT:
				self.running = False
			if event.type == pg.KEYDOWN: # Key Presses
				if event.key == pg.K_ESCAPE: # Escape Key
					pg.quit()
					quit()
				if event.key == pg.K_r: # Reset - R Key
					self.playing = False
				if event.key == pg.K_e: # Testing key. Spawns a death heart.
					deathHeart = sprites.deathHeart()
					self.allSprites.add(deathHeart)
				if event.key == pg.K_SPACE and self.player.bombs > 0: # Bombs
					self.player.bombs -= 1
					self.wipeEnemies()
				if event.key == pg.K_h: # Hard mode
					self.hardMode = True
				if event.key == pg.K_z: # Developer mode. Not to be used in actual game
					if self.developer == False:
						self.developer = True
						self.timing = False
					elif self.developer == True:
						self.developer = False
						self.player.maxLives = 5
						self.player.lives = 3
						self.player.bombs = 2
						self.currentTime = 0
						self.lastTime = time.time()
						self.startTime = pg.time.get_ticks()
						self.timing = True
		for enemy in self.enemySprites: # Player collisions
			self.enemyHits = pg.sprite.spritecollideany(self.player, self.enemySprites)
			if self.enemyHits:
				if self.enemyHits.timeAlive <= 1:
					self.enemyHits.kill()
					break
				self.enemyHits.attack()
				self.enemyHits.kill()
				self.player.enemiesHit += 1
		if self.player.lives <= 0: # Kill player
			self.playing = False
		
		if float(self.timeAlive) > float(self.highscore):
			self.highscore = self.timeAlive
			with open(HS_FILE, "w") as f:
				f.write(self.highscore)
		
		if self.developer == True: # Developer mode settings
			self.player.maxLives = 9999
			self.player.lives = self.player.maxLives
			self.player.bombs = 9999
	

	def timer(self):
		if self.timing:
			self.currentTime = (pg.time.get_ticks() - self.startTime)
			self.clock.tick(FPS)
			self.timeAlive = str(round(self.currentTime / 1000, 1))

	def gameScreen(self):
		self.screen.fill(BACKGROUND)
		self.allSprites.draw(self.screen)
		self.drawText(str(self.timeAlive), 40-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/8, False)
		if not self.developer:
			pg.draw.rect(self.screen, RED, pg.Rect(self.player.pos.x - 110, self.player.pos.y+75, (self.player.maxLives*3) * (self.player.lives*3), 25))
		self.drawText(f"Highscore: {str(self.highscore)}", 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/6, False)
		self.drawText(f"Lives: {self.player.lives}/{self.player.maxLives}", 40-TEXTDIFFERENCE, WHITE, WIDTH/6, HEIGHT/8, False)
		self.drawText(f"Bombs: {self.player.bombs}", 40-TEXTDIFFERENCE, WHITE, WIDTH-WIDTH/6, HEIGHT/8, False)
		self.drawText(f"Hard Mode: {self.hardMode}", 40-TEXTDIFFERENCE, WHITE, WIDTH-WIDTH/3, HEIGHT/8, False)
		self.drawText(f"Enemies: {len(self.enemySprites)}", 40-TEXTDIFFERENCE, WHITE, WIDTH/3, HEIGHT/8, False)
		pg.display.flip()

	def startScreen(self):
		self.screen.fill(BACKGROUND)
		self.drawText(TITLE, 60-TEXTDIFFERENCE, TITLECOLOUR, WIDTH/2, HEIGHT/4, True)
		self.drawText("Made by Ethan Bell", 40-TEXTDIFFERENCE, TITLECOLOUR, WIDTH/2, HEIGHT/4+70, False)
		self.drawText(DESCRIPTION, 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/2, False)
		self.drawText(DESCRIPTION2, 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/2+30, False)
		self.drawText("Controls", 35-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT-HEIGHT/3-50, True)
		self.drawText("Move your mouse to move the player", 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT-HEIGHT/3-20, False)
		self.drawText("Press SPACE to use your bombs", 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT-HEIGHT/3+10, False)
		self.drawText("Press H to turn on hard mode. It cannot be turned off unless you restart.", 30-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT-HEIGHT/3+40, False)
		self.drawText("Press Any Key to Start", 30-TEXTDIFFERENCE, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 20, True)
		pg.display.flip()
		self.waitForKey()
	
	def gameOverScreen(self):
		self.screen.fill(BACKGROUND)
		self.drawText(TITLE, 60-TEXTDIFFERENCE, TITLECOLOUR, WIDTH/2, HEIGHT/4, True)
		self.drawText("Made by Ethan Bell", 40-TEXTDIFFERENCE, TITLECOLOUR, WIDTH/2, HEIGHT/4+70, False)
		self.drawText("Statistics", 50-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/2, True)
		self.drawText(f"Enemies Hit: {self.player.enemiesHit}", 40-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/2+70, False)
		self.drawText(f"Time Survived: {self.timeAlive}", 40-TEXTDIFFERENCE, WHITE, WIDTH/2, HEIGHT/2+140, False)
		self.drawText("Press Any Key to Continue", 30-TEXTDIFFERENCE, WHITE, WIDTH / 2, HEIGHT * 3 / 4, True)
		pg.display.flip()
		self.waitForKey()

	def waitForKey(self): # Wait for key input
		waiting = True
		while waiting:
			self.clock.tick(FPS / 2)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						pg.quit()
						quit()
					waiting = False

	def drawText(self, text, size, colour, x, y, underlined):
		textfont = pg.font.Font(self.font_name, size)
		textfont.underline = underlined
		textSurface = textfont.render(text, True, colour)
		textRect = textSurface.get_rect()
		textRect.midtop = (x, y)
		self.screen.blit(textSurface, textRect)

g = Game()

while g.running:  
	g.startScreen()
	g.new()
	g.gameOverScreen()

pg.quit()

