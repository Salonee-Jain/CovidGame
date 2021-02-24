import pygame
import random
import math
from pygame import mixer


# initialize the module
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# background
bg = pygame.image.load("images/new.png")
mixer.music.load("shoot.wav")
mixer.music.play(-1)

# title and icon and bg
pygame.display.set_caption("Corona killer")
icon = pygame.image.load("images/hand-sanitizer.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("images/antibacterial-gel.png")
ply_X = 370
ply_Y = 480
ply_X_change = 0

# enemy
enemy_img = []
enemy_X = []
enemy_Y = []
enemy_change_X = []
enemy_change_Y = []
num_enemy = 6

for i in range(num_enemy):
    enemy_img.append(pygame.image.load("images/virus.png"))
    enemy_X.append(random.randint(0, 735))
    enemy_Y.append(random.randint(30, 150))
    enemy_change_X.append(3)
    enemy_change_Y.append(40)

# bullet
# ready-cant see bullet on screen
# fire-bullet moving
bullet_img = pygame.image.load("images/share.png")
bullet_X = 0
bullet_Y = 480
bullet_change_X = 0
bullet_change_Y = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font("basketball.otf",35)
textx = 10
texty = 10

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x, y))


def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt((math.pow(enemy_X - bullet_X, 2)) + (math.pow(enemy_Y - bullet_Y, 2)))
    if distance < 27:
        return True
    else:
        return False


# create an infinite loop
running = True
while running:
    # rgb-(red green blue)
    screen.fill((0, 0, 0))

    # background
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                ply_X_change = -5
            if event.key == pygame.K_RIGHT:
                ply_X_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_X = ply_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                ply_X_change = 0

    # checking limited boundies
    ply_X += ply_X_change
    if ply_X <= 0:
        ply_X = 0
    elif ply_X >= 736:
        ply_X = 736

    for i in range(num_enemy):
        enemy_X[i] += enemy_change_X[i]

        if enemy_X[i] <= 0:
            enemy_change_X[i] = 3
            enemy_Y[i] += enemy_change_Y[i]

        elif enemy_X[i] >= 736:
            enemy_change_X[i] = -3
            enemy_Y[i] += enemy_change_Y[i]

        collision = isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            bullet_Y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_X[i] = random.randint(0, 735)
            enemy_Y[i] = random.randint(30, 150)
        enemy(enemy_X[i], enemy_Y[i], i)
    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = "ready"

    if bullet_state is 'fire':
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_change_Y

    player(ply_X, ply_Y)
    show_score(textx, texty)
    pygame.display.update()
