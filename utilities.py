import math
import pygame

DRAG_POWER = .3
COUNTDOWN_TICKS_PER_SECOND = 40 #Ticks per second of gameplay

PLANET_SIZE = 100
MAP_SIZE = 200
SCREEN_SIZE = [800,600]

def rotateAroundPoint(img, radians, point = -1):
    if point == -1:
        point = img.get_rect().center
    ret_img = pygame.transform.rotate(img, radians * 180/math.pi)
    ret_img.get_rect().center = point
    return ret_img

def coordToDegree(x, y):
    r = math.atan2(y, x)
    h = math.dist([0,0], [x, y])
    return r, h

def moveCloser(start, end, step = 1):
    step = abs(step)
    if start < end:
        start += step
        if start > end:
            return end
    elif start > end:
        start -= step
        if start < end:
            return end
    return start

def isPointingAt(pointA, rotA, pointB, closeness = 0):
    a = orient(pointA, rotA, pointB, closeness)
    return a == rotA
        
    

def orient(position, rotation, goal, speed = 2*math.pi/10):
    # Get degree from current position to target
    goal[0] -= position[0]
    goal[1] -= position[1]
    goal = math.atan2(goal[1], goal[0])

    # Orient self to face target
    if math.dist([goal], [rotation]) > math.dist([goal-2*math.pi], [rotation]):
        goal -= 2*math.pi
    elif math.dist([goal], [rotation]) > math.dist([goal+2*math.pi], [rotation]):
        goal += 2*math.pi

    if goal == rotation: return goal

    if goal > rotation:
        rotationB = rotation + speed
    else:
        rotationB = rotation - speed
    
    if math.dist([rotationB], [goal]) < math.dist([rotation], [goal]):
        return rotationB
    return goal


def drag(velocity):
    def _drag(spd):
        if spd == 0: return 0
        sign = 1 if spd > 0 else -1
        return sign * max(abs(spd) - DRAG_POWER, 0)
            
    velocity[0] = _drag(velocity[0])
    velocity[1] = _drag(velocity[1])
    return velocity