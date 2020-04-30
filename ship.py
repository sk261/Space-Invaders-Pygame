from utilities import orient, COUNTDOWN_TICKS_PER_SECOND, drag, moveCloser, isPointingAt
from math import pi, cos, sin, dist

class Ship:
    def __init__(self):
        self.pos = [0,0]
        self.velocity = [0,0]
        self.speed = 0
        self.strafeSpd = 0
        self.maxSpeedTime = .2
        self.rotation = 0
        self.firingMode = 0
        self.imageSet = []
        self.activeImage = -1
        self.imageCycle = []
        self._cycledImageIndex = 0
        self.rotationalSpeed = 0

    def tick(self):

        self.rotation += self.rotationalSpeed

        while self.rotation < 0: self.rotation += 2*pi
        self.rotation %= 2*pi

        # Velocity to position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Linear movement
        jump = 0
        if self.speed != 0:
            jump = self.speed / (COUNTDOWN_TICKS_PER_SECOND * self.maxSpeedTime)
        # Strafe movement
        strafe = 0
        if self.strafeSpd != 0:
            strafe = self.strafeSpd / (COUNTDOWN_TICKS_PER_SECOND * self.maxSpeedTime)
        # Create a 'step' size based on the average
        step = abs(jump) + abs(strafe)
        _x = (cos(self.rotation) * jump) + (cos(self.rotation + pi/2) * strafe)
        _y = (sin(self.rotation) * jump) + (sin(self.rotation + pi/2) * strafe)

        if step != 0:
            self.velocity[0] = moveCloser(self.velocity[0], _x, step)
            self.velocity[1] = moveCloser(self.velocity[1], _y, step)
        elif step == 0:
            # Drag velocity
            self.velocity = drag(self.velocity)

    def addImage(self, img, isCycle = False):
        self.imageSet.append(img)
        if isCycle:
            self.imageCycle.append(len(self.imageSet)-1)

    def Position(self):
        return [self.pos[0], self.pos[1]]

    def Velocity(self):
        return [self.velocity[0], self.velocity[1]]
    
    def getCycleImage(self):
        if len(self.imageCycle) > 0:
            self._cycledImageIndex += 1
            if self._cycledImageIndex >= len(self.imageCycle):
                self._cycledImageIndex = 0
            return self.imageSet[self.imageCycle[self._cycledImageIndex]]
        return False

    def getImage(self):
        if len(self.imageSet) == 0 or self.activeImage < 0 or self.activeImage >= len(self.imageSet):
            return False
        return self.imageSet[self.activeImage]

    @property
    def x(self):
        return self.pos[0]
    
    @property
    def y(self):
        return self.pos[1]
    
    @x.setter
    def x(self, value):
        self.pos[0] = value
    
    @y.setter
    def y(self, value):
        self.pos[1] = value

class Player(Ship):
    def __init__(self, idle, laser, homing, bullet):
        super(Player, self).__init__()
        self.addImage(idle)
        self.addImage(bullet)
        self.addImage(homing)
        self.addImage(laser)
        self.idleTimer = 0
        self.strafeCD = 0
        self.strafeMaxCD = COUNTDOWN_TICKS_PER_SECOND
        self.weapon = 0
        self.firing = False
        self.firingCD = 0
        self.disabledCD = 0
        self.firingTime = 0
        self.maxFiringTime = COUNTDOWN_TICKS_PER_SECOND * 2
        self.maxFiringTimeCD = COUNTDOWN_TICKS_PER_SECOND * 1
        self.bulletCount = 0
        self.firedBullets = []
    
    def getFiringMaxCD(self):
        if self.weapon == 0: # Bullet
            # 5 shots/second
            return COUNTDOWN_TICKS_PER_SECOND * .2
        elif self.weapon == 1: # Homing
            # 10 shots/second
            return COUNTDOWN_TICKS_PER_SECOND * .1
        else: # LASER
            return COUNTDOWN_TICKS_PER_SECOND
            

    def getImg(self):
        if self.firing or self.disabledCD > 0:
            if self.weapon == 2 or self.disabledCD > 0:
                return self.getLaser()
            elif self.weapon == 0:
                return self.getBullet()
            elif self.weapon == 1:
                return self.getHoming()
        return self.getIdle()
    
    def getIdle(self):
        self.activeImage = 0
        return self.getImage()

    def getBullet(self):
        self.activeImage = 1
        return self.getImage()

    def getHoming(self):
        self.activeImage = 2
        return self.getImage()

    def getLaser(self):
        self.activeImage = 3
        return self.getImage()
    
    def tick(self):
        tempStrafe = self.strafeSpd
        tempSpd = self.speed
        tempRot = self.rotationalSpeed
        if self.strafeCD > 0:
            self.strafeCD -= 1
            self.strafeSpd = 0

        if self.firing:
            self.firingTime += 1
        else:
            self.firingTime = 0

        if self.firingCD <= 0 and self.firing:
            self.firingCD = self.getFiringMaxCD()
            if self.weapon == 2:
                self.disabledCD = self.getFiringMaxCD()
            elif self.weapon == 1:
                if self.firingTime > self.maxFiringTime:
                    self.firingCD = self.maxFiringTimeCD
                    self.firingTime = -self.firingCD
            self.bulletCount += 1
            pos = self.Position()
            if self.weapon == 0: # Bullet
                if self.bulletCount % 3 == 0:
                    pos = [pos[0] - cos(self.rotation)*25, pos[1] - sin(self.rotation)*25] # Tip
                elif self.bulletCount % 3 == 1:
                    pos = [pos[0] - cos(self.rotation-1.21202)*25, pos[1] - sin(self.rotation-1.21202)*25] # Left
                else:
                    pos = [pos[0] - cos(self.rotation+1.21202)*25, pos[1] - sin(self.rotation+1.21202)*25] # Right
            elif self.weapon == 2: # Laser
                pos = [pos[0] - cos(self.rotation)*25, pos[1] - sin(self.rotation)*25] # Tip
                
            self.firedBullets.append([self.weapon, self.rotation, pos, self.Velocity()])
        elif self.firingCD > 0:
            self.firingCD -= 1

        if self.disabledCD > 0:
            self.disabledCD -= 1
            self.speed = 0
            self.strafeSpd = 0
            self.rotationalSpeed = 0

        super(Player, self).tick()

        if self.strafeSpd != 0:
            self.strafeCD = self.strafeMaxCD
        self.strafeSpd = tempStrafe
        self.speed = tempSpd
        self.rotationalSpeed = tempRot 

class Kamakazi(Ship):
    def __init__(self, idle, cycle1, cycle2, cycle3, player = None):
        super(Kamakazi, self).__init__()
        self.addImage(idle)
        self.addImage(cycle1, True)
        self.addImage(cycle2, True)
        self.addImage(cycle3, True)
        self.target = player
        self.max_cooldown = COUNTDOWN_TICKS_PER_SECOND * 2
        self.cooldown = self.max_cooldown
        self.triggered = False
        self.spinSpeed = pi/320

    def getImg(self):
        if self.triggered:
            return self.getFlying()
        else:
            return self.getIdle()
    
    def getIdle(self):
        self.activeImage = 0
        return self.getImage()
    
    def getFlying(self):
        return self.getCycleImage()
    
    def tick(self):
        super(Kamakazi, self).tick()
        if self.triggered:
            self.cooldown -= 1
            if self.cooldown > 0:
                self.speed = 60
            else:
                self.speed = 0
                self.triggered = False
                self.cooldown = self.max_cooldown
                # Stop going
        newRot = orient(self.pos, self.rotation, self.target.Position(), self.spinSpeed)
        if not self.triggered:
            self.rotation = newRot
            if isPointingAt(self.Position(), self.rotation, self.target.Position(), self.spinSpeed):
                self.triggered = True


class Mini(Ship):
    def __init__(self, img, target = None):
        super(Mini, self).__init__()
        self.addImage(img)
        self.speed = 15 # Just barely slower than the player
        self.target = target
        self.spinSpeed = pi/64

    def getImg(self):
        return self.getFlying()
    
    def getFlying(self):
        self.activeImage = 0
        return self.getImage()
    
    def tick(self):
        super(Mini, self).tick()
        newRot = orient(self.pos, self.rotation, self.target.Position(), self.spinSpeed)
        self.rotation = newRot

class Mother(Ship):
    def __init__(self, img, cycle1, cycle2, cycle3, target = None):
        super(Mother, self).__init__()
        self.addImage(img)
        self.addImage(cycle1, True)
        self.addImage(cycle2, True)
        self.addImage(cycle3, True)
    
    def getSpawnShip(self):
        return self.getCycleImage()
    
