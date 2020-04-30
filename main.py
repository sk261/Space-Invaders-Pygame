import math
import random
import resources
import game
import ship

import utilities
from utilities import coordToDegree, rotateAroundPoint
import pygame
from pygame import mixer, time

WINDOW_SIZE = [800, 600]

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))

# Framerate
clock = pygame.time.Clock()

# Background
background = resources.backgroundImg

# Sound
#mixer.music.load(resources.backgroundSound)
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Shay's Space Invader")
icon = resources.iconImg
pygame.display.set_icon(icon)

# Player
playerImg = resources.playerImg
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(resources.enemyImg)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = resources.bulletImg
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
font = pygame.font.Font('freesansbold.ttf', 32)


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(val):
    score = font.render("Score: " + str(val), True, (255,255,255))
    screen.blit(score, (5, 5))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    over_text = font.render("Press N to restart", True, (255, 255, 255))
    screen.blit(over_text, (220, 320))

session = game.Game()
_enemy = ship.Kamakazi(resources.kamakaziImg, resources.kamakazi_1, resources.kamakazi_2, resources.kamakazi_3)
session.spawnShip(_enemy)

for n in range(30):
    _enemy = ship.Mini(resources.miniImg)
    session.spawnShip(_enemy)


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    # Background Image
#    screen.blit(img, (200-img.get_rect().center[0], 200-img.get_rect().center[1]))
#    screen.set_at([200,200], (255,0,0))
#    screen.set_at([int(200+session.player.x), int(200+session.player.y)], (0,255,0))
#    r, h = coordToDegree(session.player.x, session.player.y)
#    screen.set_at([200, (200-int(h))], (0,255,0))
    session.tick()

    while len(session.enemies) < 30:
        if random.randint(0, 9) == 0:
            _enemy = ship.Kamakazi(resources.kamakaziImg, resources.kamakazi_1, resources.kamakazi_2, resources.kamakazi_3)
        else:
            _enemy = ship.Mini(resources.miniImg)
        session.spawnShip(_enemy)
    
    triggers = {}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                triggers["left"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_RIGHT:
                triggers["right"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_UP:
                triggers["up"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_DOWN:
                triggers["down"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_q:
                triggers["q"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_e:
                triggers["e"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_1:
                triggers["1"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_2:
                triggers["2"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_3:
                triggers["3"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_SPACE:
                triggers["space"] = event.type == pygame.KEYDOWN
            if event.key == pygame.K_n:
                triggers["n"] = event.type == pygame.KEYDOWN

    session.triggerInput(triggers)

    # Player
    screen.blit(session.draw(), [0,0])

    if session.gameOver:
        game_over_text()
    show_score(session.score)

    pygame.display.update()
    clock.tick(utilities.COUNTDOWN_TICKS_PER_SECOND)
