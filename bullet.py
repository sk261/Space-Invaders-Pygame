import math
from utilities import orient, COUNTDOWN_TICKS_PER_SECOND, moveCloser, drag
from pygame import draw
import random

PROJECTILE_TYPE_BULLET = 1
PROJECTILE_TYPE_HOMING = 2
PROJECTILE_TYPE_LASER = 3

class Bullet:
    def __init__(self, projectile, rotation, position, velocity, targets = False):
        self._type = projectile
        self.position = position
        self.rotation = rotation + math.pi
        self.targets = []
        self.target = False
        self.firingDelay = 0
        if targets != False:
            if len(targets) > 0:
                self.target = random.choice(targets)
                self.targets = targets
        self.countdown = COUNTDOWN_TICKS_PER_SECOND * 1 # 1 second countdown

        self.speed = math.atan2(velocity[0], velocity[1])

        firing_velocity = [math.cos(self.rotation), math.sin(self.rotation)]

        if self._type == PROJECTILE_TYPE_BULLET:
            self.speed = 30
            step = self.speed / (COUNTDOWN_TICKS_PER_SECOND * .2)
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * 5 #Lasts 5 seconds
            self.velocity = [firing_velocity[0]*step, firing_velocity[1]*step]
            self.firingDelay = .5 * COUNTDOWN_TICKS_PER_SECOND
            # Bullet continues straight based on rotation and starting velocity
        elif self._type == PROJECTILE_TYPE_HOMING:
            self.speed = 30

            step = 1 + (random.randint(1,20) / 10) * self.speed / (COUNTDOWN_TICKS_PER_SECOND * .2)
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * 5 #Lasts 3 seconds
            self.firingDelay = COUNTDOWN_TICKS_PER_SECOND * 2 #2 second firing delay

            self.rotation += random.randint(-135,135) + 180
            firing_velocity = [math.cos(self.rotation), math.sin(self.rotation)]
            self.velocity = [firing_velocity[0]*step, firing_velocity[1]*step]
            # Bullet rotates to reach target, much like a kamakazi ship
        elif self._type == PROJECTILE_TYPE_LASER:
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * .8 #Lasts 8/10ths of a second seconds
            # Do nothing because everything in front of you is about to die (except shields)

        self.maxCD = self.countdown

    def updateTargets(self, targets):
        self.targets = targets
        if self.firingDelay > 0:
            self.target = None
            return
        if self.target != None:
            if not self.target in self.targets:
                self.target = None
        if len(self.targets) > 0 and (self.target == False or self.target == None):
            closest = math.dist(self.position, targets[0].Position())
            index = 0
            for n in range(len(targets)):
                a = math.dist(self.position, targets[n].Position())
                if a < closest and random.randint(0,1) != 0:
                    closest = a
                    index = n
            self.target = targets[index]

    # Returns True if the countdown has ended and object is destroyed
    def tick(self):
        self.countdown -= 1
        if self._type == PROJECTILE_TYPE_BULLET:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
        elif self._type == PROJECTILE_TYPE_HOMING:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            if self.firingDelay > 0:
                self.firingDelay -= 1
                self.velocity = drag(self.velocity)
                return False
            # If a target is no selected, then it fires off like a normal bullet
            if self.target != False and self.target != None:
                newRot = orient(self.position, self.rotation, self.target.Position(), 2*math.pi/10)
                self.rotation = newRot
                while self.rotation < 0: self.rotation += 2*math.pi
                self.rotation %= 2*math.pi

                step = self.speed / (COUNTDOWN_TICKS_PER_SECOND * .2)

                self.velocity[0] = moveCloser(self.velocity[0], math.cos(self.rotation) * step, step)
                self.velocity[1] = moveCloser(self.velocity[1], math.sin(self.rotation) * step, step)
            else:
                if len(self.targets) > 0:
                    self.target = random.choice(targets)


            # Time slows while selecting
            # Target is selected
            # Bullets curve to target

#        elif self._type == PROJECTILE_TYPE_LASER:
            # Player ship stops responding for 1 second
            # Player ship receives reverse velocity
            # All ships cut accross laser are cut in half
            # Laser fades away in .8 seconds

        if self.countdown <= 0:
            return True
        return False
        
    def draw(self, surface, offsetX = 0, offsetY = 0):
        _x = self.position[0] + offsetX
        _y = self.position[1] + offsetY
        size = 2
        colour = (255, 255, 255)
        if self._type == PROJECTILE_TYPE_LASER:
            size = 1000
            colour = (255,0,0)
        elif self._type == PROJECTILE_TYPE_BULLET:
            colour = (0,255,0)
        elif self._type == PROJECTILE_TYPE_HOMING:
            colour = (0,255,255)
        e_x = math.cos(self.rotation) * size + _x
        e_y = math.sin(self.rotation) * size + _y

        draw.line(surface, colour, (_x, _y), (e_x, e_y), 1)
        






