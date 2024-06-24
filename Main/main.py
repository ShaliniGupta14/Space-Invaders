import pygame
import random
import math
from pygame import mixer

#Initialize pygame
pygame.init()

#Game window
screen = pygame.display.set_mode((800, 600))

#Background Image
background_image = pygame.image.load('background.png')

#Background sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
player_IMG = pygame.image.load('player.png')
playerX = 370
playerY = 490
playerX_change = 0

#Enemy
enemy_list = ['alien1.png', 'alien2.png', 'alien3.png', 'alien4.png', 'alien5.png', 'monster.png']

enemy_IMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(0, num_of_enemies):
    image = random.randint(0, 5)
    enemy_IMG.append(pygame.image.load(enemy_list[image]))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(25, 300))
    enemyX_change.append(0.85)
    enemyY_change.append(20)

#Bullet
bullet_IMG = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game
over_font = pygame.font.Font('freesansbold.ttf', 64 )

def show_score(x, y):
    score =  font.render("Score : " + str(score_value), True, (0, 128, 128))
    screen.blit(score, (x, y))

def game_over():
    over_text = over_font.render("GAME OVER", True, (0, 128, 128))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_IMG, (x, y))

def enemy_spawner(i):
    enemy_list = ['alien1.png', 'alien2.png', 'alien3.png', 'alien4.png', 'alien5.png', 'monster.png']
    image = random.randint(0, 5)
    enemy_IMG[i] = pygame.image.load(enemy_list[image])
    enemyX[i] = random.randint(0, 736)
    enemyY[i] = random.randint(25, 300)

def enemy(x, y, i):
    screen.blit(enemy_IMG[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_IMG, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False

#Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Player Movement
    playerX = playerX + playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bulletY < -5:
        bulletY = 490
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #Enemy Movement
    for i in range(0, num_of_enemies):
        #Game_Over
        if enemyY[i] > 430:
            for j in range(0, num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.9
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.9
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.mp3")
            collision_sound.play()
            bulletY = 490
            bullet_state = "ready"
            score_value += 1
            enemy_spawner(i)

        enemy(enemyX[i], enemyY[i], i)


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
