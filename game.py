import math
import utilities
import resources
import ship
import pygame
from bullet import Bullet, PROJECTILE_TYPE_LASER
import random

class Game:
    def __init__(self):
        self.player = ship.Player(resources.playerImg, resources.playerLaserImg, resources.playerHomingImg, resources.playerBulletImg)
        self.player.y = -(utilities.PLANET_SIZE + 10)
        self.currentTriggers = []
        
        self.bullets = []
        self.enemies = []

        self.explosionTime = .3 * utilities.COUNTDOWN_TICKS_PER_SECOND
        self.explosions = []
        self.score = 0

        self.gameOver = False

    def spawnShip(self, ship):
        rot = random.randint(0, 360) * math.pi / 180
        ship.pos = [utilities.MAP_SIZE * math.cos(rot), utilities.MAP_SIZE * math.sin(rot)]
        ship.target = self.player
        self.enemies.append(ship)
    
    def _checkBullet(self, bullet):
        n = 0
        while n < len(self.enemies):
            if bullet._type == PROJECTILE_TYPE_LASER:
                d = math.dist(bullet.position, self.enemies[n].Position())
                _pos = (bullet.position[0] + math.cos(bullet.rotation) * d, bullet.position[1] + math.sin(bullet.rotation) * d)
                if math.dist(_pos, self.enemies[n].Position()) < self.enemies[n].getImg().get_rect().width:
                    self.explosions.append([(self.enemies[n].Position()[0], self.enemies[n].Position()[1]), 0])
                    self.score += 1
                    del self.enemies[n]
                    continue
            else:
                d = math.dist(bullet.position, self.enemies[n].Position())
                if d < 30: # General comparison to check if it's close without testing image
                    if d < self.enemies[n].getImg().get_rect().width:
                        self.score += 1
                        del self.enemies[n]
                        return True
            n += 1
        return False
    
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
        if 'n' in keys:
            if self.gameOver:
                self.gameOver = False
                self.__init__()

    
    def tick(self):
        self.handleControls()
        if self.gameOver:
            return True

        # Player and bullets
        self.player.tick()

        n = 0
        while n < len(self.bullets):
            self.bullets[n].updateTargets(self.enemies)
            if not self.bullets[n].tick():
                if not self._checkBullet(self.bullets[n]):
                    n += 1
                    continue
            if self.bullets[n]._type != PROJECTILE_TYPE_LASER:
                self.explosions.append([(self.bullets[n].position[0], self.bullets[n].position[1]), 0])
            del self.bullets[n]

        for n in self.player.firedBullets:
            bulletType = n[0] + 1
            target = None
            self.bullets.append(Bullet(bulletType, n[1], n[2], n[3], self.enemies))
        
        self.player.firedBullets = []


        # Enemies
        for n in self.enemies:
            n.tick()
            if math.dist(n.Position(), self.player.Position()) < n.getImg().get_rect().width / 2 + self.player.getImg().get_rect().width / 2:
                self.gameOver = True
                return True

        # Explosions
        n = 0
        while n < len(self.explosions):
            if self.explosions[n][1] >= self.explosionTime:
                del self.explosions[n]
                continue
            self.explosions[n][1] += 1
            n += 1

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

        for n in self.explosions:
            img = pygame.Surface((11, 11), pygame.SRCALPHA)
            img.fill((0,0,0,0))
            a = int(max(0, 255 * (1 - (n[1] / self.explosionTime))))
            pygame.draw.circle(img, (255,0,0,a), (5, 5), 5)
            
            ret.blit(img, (_x + n[0][0] - 5, _y + n[0][1] - 5))
        
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
    
    