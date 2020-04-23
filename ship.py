from utilities import orient, COUNTDOWN_TICKS_PER_SECOND, drag

class Ship:
    def __init__(self):
        self.pos = [0,0]
        self.velocity = [0,0]
        self.speed = 0
        self.rotation = 0
        self.firingMode = 0
        self.imageSet = []
        self.activeImage = -1
        self.imageCycle = []
        self._cycledImageIndex = 0

    def tick(self):
        self.velocity = drag(self.velocity)

    def addImage(self, img, isCycle = False):
        self.imageSet.append(img)
        if isCycle:
            self.imageCycle.append(len(self.imageSet)-1)

    def Position(self):
        return [self.pos[0], self.pos[1]]
    
    def getCycleImage(self):
        if len(self.imageCycle) > 0:
            _cycledImageIndex += 1
            if _cycledImageIndex >= len(self.imageCycle):
                _cycledImageIndex = 0
            return self.imageCycle[_cycledImageIndex]
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

class Kamakazi(Ship):
    def __init__(self, idle, cycle1, cycle2, cycle3, player):
        super(Kamakazi, self).__init__()
        self.addImage(idle)
        self.addImage(cycle1, True)
        self.addImage(cycle2, True)
        self.addImage(cycle3, True)
        self.target = player
        self.max_cooldown = COUNTDOWN_TICKS_PER_SECOND * 2
        self.cooldown = self.max_cooldown
        self.triggered = False
    
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
        

        newRotation = orient(self.position, self.rotation, self.target, 2*math.pi/10)


class Mini(Ship):
    def __init__(self, img):
        super(Mini, self).__init__()
        self.addImage(img)
    
    def getFlying(self):
        self.activeImage = 0
        return self.getImage()

class Mother(Ship):
    def __init__(self, img, cycle1, cycle2, cycle3):
        super(Mother, self).__init__()
        self.addImage(img)
        self.addImage(cycle1, True)
        self.addImage(cycle2, True)
        self.addImage(cycle3, True)
    
    def getSpawnShip(self):
        return self.getCycleImage()
    
