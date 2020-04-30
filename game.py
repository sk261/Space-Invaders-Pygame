import math
import utilities
import resources
import ship
import pygame
from bullet import Bullet

class Game:
    def __init__(self):
        self.player = ship.Player(resources.playerImg, resources.playerLaserImg, resources.playerHomingImg, resources.playerBulletImg)
        self.player.y = -(utilities.PLANET_SIZE + 10)
        self.currentTriggers = []
        
        self.bullets = []
        self.enemies = []

    def spawnShip(self, ship):
        self.enemies.append(ship)
    
    def triggerInput(self, triggers):
        if len(triggers) == 0: return
        for n in triggers.keys():
            if n in self.currentTriggers and not triggers[n]:
                self.currentTriggers.remove(n)
            elif triggers[n] and not (n in self.currentTriggers):
                self.currentTriggers.append(n)
    
    def handleControls(self):
        keys = self.currentTriggers
        self.player.speed = 0
        self.player.rotationalSpeed = 0
        self.player.strafeSpd = 0
        self.player.firing = False
        if 'up' in keys:
            self.player.speed = -20
        if 'down' in keys:
            self.player.speed = 20
        if 'right' in keys:
            self.player.rotationalSpeed = math.pi/32
        if 'left' in keys:
            self.player.rotationalSpeed = -math.pi/32
        if '1' in keys:
            self.player.weapon = 0
        if '2' in keys:
            self.player.weapon = 1
        if '3' in keys:
            self.player.weapon = 2
        if 'space' in keys:
            self.player.firing = True
        if 'q' in keys:
            self.player.strafeSpd = 50
        if 'e' in keys:
            self.player.strafeSpd = -50

    
    def tick(self):
        self.handleControls()

        # Player and bullets
        self.player.tick()

        n = 0
        while n < len(self.bullets):
            if not self.bullets[n].tick():
                n += 1
                continue
            del self.bullets[n]

        for n in self.player.firedBullets:
            bulletType = n[0] + 1
            self.bullets.append(Bullet(bulletType, n[1], n[2], n[3], False))
        
        self.player.firedBullets = []


        # Enemies
        for n in self.enemies:
            n.tick()

    def draw(self):
        ret = getBackgroundImage(self.player.x, self.player.y)
        # Player
        img = utilities.rotateAroundPoint(self.player.getImg(), math.pi/2 - self.player.rotation)
        ret.blit(img, (utilities.SCREEN_SIZE[0]/2-img.get_rect().center[0], utilities.SCREEN_SIZE[1]/2-img.get_rect().center[1]))
        # Bullets
        # Offset
        _x = utilities.SCREEN_SIZE[0]/2-self.player.x
        _y = utilities.SCREEN_SIZE[1]/2-self.player.y
        for n in self.bullets:
            n.draw(ret, _x, _y)
        
        for n in self.enemies:
            img = n.getImg()
            img = utilities.rotateAroundPoint(n.getImg(), 3*math.pi/2 - n.rotation)
            ret.blit(img, (_x+n.Position()[0]-img.get_rect().center[0], _y+n.Position()[1]-img.get_rect().center[1]))
        
        return ret


        

def regularizePosition(x):
    circ = 2 * math.pi * utilities.PLANET_SIZE/2
    while x < 0:
        x += circ
    while x >= circ:
        x -= circ


def getBackgroundImage(x, y):
    # Move planet based on X, Y of the player
    world = pygame.transform.scale(resources.worldImg, (2*utilities.PLANET_SIZE, 2*utilities.PLANET_SIZE))


    bg = pygame.Surface((utilities.SCREEN_SIZE[0], utilities.SCREEN_SIZE[1]))
    bg.fill((102, 0, 148))
    _x = utilities.SCREEN_SIZE[0]/2-world.get_rect().center[0]-x
    _y = utilities.SCREEN_SIZE[1]/2-world.get_rect().center[1]-y
    if (_x > -utilities.PLANET_SIZE and _x < utilities.SCREEN_SIZE[0] + utilities.PLANET_SIZE
        and _y > -utilities.PLANET_SIZE and _y < utilities.SCREEN_SIZE[1] + utilities.PLANET_SIZE):
        bg.blit(world, (_x, _y))
    
    

    return bg
    
    # Create image the size of the screen
    # Draw background colour
    # Draw world to World size
    # Draw gradient from the world to Map size
    
    