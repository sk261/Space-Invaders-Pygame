import math
from utilities import orient, COUNTDOWN_TICKS_PER_SECOND

PROJECTILE_TYPE_BULLET = 1
PROJECTILE_TYPE_HOMING = 2
PROJECTILE_TYPE_LASER = 3

class Bullet:
    def __init__(self, projectile, rotation, position, velocity, target = False):
        self._type = projectile
        self.position = position
        self.rotation = rotation
        self.target = target
        self.countdown = COUNTDOWN_TICKS_PER_SECOND * 1 # 1 second countdown

        self.speed = math.atan2(velocity[0], velocity[1])

        firing_velocity = [math.cos(rotation), math.sin(rotation)]

        if self._type == PROJECTILE_TYPE_BULLET:
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * 5 #Lasts 3 seconds
            self.speed += 6
            self.velocity = [firing_velocity[0]*self.speed, firing_velocity[1]*self.speed]
            # Bullet continues straight based on rotation and starting velocity
            continue
        elif self._type == PROJECTILE_TYPE_HOMING:
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * 3 #Lasts 3 seconds
            self.speed += 3
            self.velocity = [firing_velocity[0]*self.speed, firing_velocity[1]*self.speed]
            # Bullet rotates to reach target, much like a kamakazi ship
            continue
        elif self._type == PROJECTILE_TYPE_LASER:
            self.countdown = COUNTDOWN_TICKS_PER_SECOND * .8 #Lasts 8/10ths of a second seconds
            # Do nothing because everything in front of you is about to die (except shields)
            continue

    # Returns True if the countdown has ended and object is destroyed
    def tick(self):
        self.countdown -= 1
        if self._type == PROJECTILE_TYPE_BULLET:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            continue
        elif self._type == PROJECTILE_TYPE_HOMING:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            # If a target is no selected, then it fires off like a normal bullet
            if self.target != False:
                self.rotation = orient(self.position, self.rotation, self.target.pos, 2*math.pi/10)
                # Set velocity to new object
                firing_velocity = [math.cos(self.rotation), math.sin(self.rotation)]
                self.velocity = [firing_velocity[0]*self.speed, firing_velocity[1]*self.speed]

            # Time slows while selecting
            # Target is selected
            # Bullets curve to target
            continue
        elif self._type == PROJECTILE_TYPE_LASER:
            # Player ship stops responding for 1 second
            # Player ship receives reverse velocity
            # All ships cut accross laser are cut in half
            # Laser fades away in .8 seconds
            continue

        if self.countdown <= 0:
            return True

