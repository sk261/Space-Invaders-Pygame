import math

DRAG_POWER = .5
COUNTDOWN_TICKS_PER_SECOND = 40 #Ticks per second of gameplay


def orient(position, rotation, goal, speed = 2*math.pi/10):
    # Get degree from current position to target
    goal[0] -= position[0]
    goal[1] -= position[1]
    d = math.dist([0,0],goal)
    goal[0] /= d
    goal[1] /= d
    goal = math.atan2(goal[1], goal[0])

    # Orient self to face target
    if goal < 0: goal += 2*math.pi
    if rotation < 0: rotation += 2*math.pi
    goal -= rotation

    ROTATION_SPEED = 2*math.pi/10

    if abs(goal) < ROTATION_SPEED:
        rotation = goal
    else:
        if goal < math.pi and goal > 0:
            rotation += ROTATION_SPEED
        else:
            rotation -= ROTATION_SPEED
    return rotation

def drag(velocity):
    def _drag(spd):
        if spd == 0: return 0
        sign = 1 if spd > 0 else -1
        return sign * max(abs(spd) - DRAG_POWER, 0)
            
    velocity[0] = _drag(velocity[0])
    velocity[1] = _drag(velocity[1])