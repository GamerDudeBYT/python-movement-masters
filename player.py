import asyncio
import sprites
import settings
        
lives = 5
speed = 10
invincible = False
playerDefault = sprites.PlayerSprite(settings.WIDTH/2, settings.HEIGHT/2, "images/slime.png")


async def damage(damage):
    if invincible:
        return
    lives -= damage

async def immortal(time):
    global invincible
    invincible = True
    await asyncio.sleep(time)
    invincible = False