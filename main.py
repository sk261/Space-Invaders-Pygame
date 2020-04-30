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
mixer.music.load(resources.backgroundSound)
mixer.music.play(-1)

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

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y, txt = -1):
    if txt == -1:
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    else:
        score = font.render(txt, True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))




def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

session = game.Game()
_enemy = ship.Kamakazi(resources.kamakaziImg, resources.kamakazi_1, resources.kamakazi_2, resources.kamakazi_3, session.player)
session.spawnShip(_enemy)
_enemy = ship.Mini(resources.miniImg, session.player)
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
                if bullet_state is "ready":
                    bulletSound = mixer.Sound(resources.laserSound)
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    session.triggerInput(triggers)

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound(resources.explosionSound)
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Player
    screen.blit(session.draw(), [0,0])

    txt = str(int(session.player.x)) + ", " + str(int(session.player.y)) + " - " + str(int(session.enemies[0].x)) + ", " + str(int(session.enemies[0].y))
    show_score(textX, testY, txt)
    pygame.display.update()
    clock.tick(utilities.COUNTDOWN_TICKS_PER_SECOND)
