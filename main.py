import pygame
import random
from pygame import mixer

# initialise the pygame
pygame.init()
# create the screen
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height)) # tuple of height and width for screen

# title and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerImg = pygame.image.load('player.png')
playerW = 64
playerH = 64
off_vert_p = 64
off_horz_p = 1
playerX = window_width/2-playerW/2
playerY = window_height-off_vert_p-playerH/2
playerSpeed = 4
dx_player = 0

# enemy
enemyImg = pygame.image.load('enemy.png')
enemyW = 64
enemyH = 64
off_vert_e = 1
off_horz_e = 1
enemyX = []
enemyY = []
dx_enemy = []
dy_enemy = []
num_enemies = 7
enemySpeed = 3
for i in range(0, num_enemies):
    enemyX.append(random.randint(1, window_width-enemyW-off_horz_e))
    enemyY.append(random.randint(off_vert_e, 150))
    dx_enemy.append(enemySpeed)
    dy_enemy.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletW = 32
bulletH = 32
bulletX = playerX+playerW/2-bulletW/2
bulletY = playerY-bulletH
state = False
dy_bullet = 5
collision_offet = 5

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def showScore(x, y):
    render_score = font.render("Score : {}".format(score), True, (0, 255, 0))
    screen.blit(render_score, (x, y))

def player(x, y):
    # blit for draw
    screen.blit(playerImg, (x, y))

def enemy(enemyX, enemyY):
    # blit for draw
    for i in range(0, num_enemies):
        screen.blit(enemyImg, (enemyX[i], enemyY[i]))

def bullet(x, y):
    screen.blit(bulletImg, (x, y))

# game loop
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx_player = -playerSpeed
                if event.key == pygame.K_RIGHT:
                    dx_player = playerSpeed
                if event.key == pygame.K_SPACE:
                    if not state:
                        bulletSound = mixer.Sound('laser.wav')
                        bulletSound.play()
                        bulletX = playerX+playerW/2-bulletW/2
                        state = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dx_player = 0
        
        # player image
        if playerX+dx_player < window_width-playerW-off_horz_p and playerX+dx_player > off_horz_p:
            playerX = playerX+dx_player        
        player(playerX, playerY)
        
        # enemy image
        for i in range(0, num_enemies):
            if enemyX[i]+dx_enemy[i] > window_width-enemyW-off_horz_e:
                dx_enemy[i] = -enemySpeed
                enemyY[i] = enemyY[i]+dy_enemy[i]
            if enemyX[i]+dx_enemy[i] < off_horz_e:
                dx_enemy[i] = enemySpeed
                enemyY[i] = enemyY[i]+dy_enemy[i] 
            enemyX[i] = enemyX[i]+dx_enemy[i]
        enemy(enemyX, enemyY)

        # enemy collides player
        for i in range(0, num_enemies):
            if enemyY[i]+enemyH+collision_offet > playerY and enemyX[i]+collision_offet < playerX+playerW and enemyX[i] > playerX+collision_offet: # right collision
                game_over = True
                collisionSound = mixer.Sound('explosion.wav')
                collisionSound.play()
            if enemyY[i]+enemyH+collision_offet > playerY and enemyX[i]+enemyW > playerX+collision_offet and enemyX[i]+enemyW < playerX+playerW-collision_offet: # left collision
                game_over = True
                collisionSound = mixer.Sound('explosion.wav')
                collisionSound.play()
        
        # bullet image
        if state:
            bulletY = bulletY-dy_bullet
            bullet(bulletX, bulletY)
        if bulletY < 0:
            state = False
            bulletX = playerX+playerW/2-bulletW/2
            bulletY = playerY-bulletH

        # bullet collides enemy
        for i in range(0, num_enemies):
            if bulletY < enemyY[i]+enemyH and bulletY > enemyY[i] and bulletX+bulletW > enemyX[i]+collision_offet and bulletX+bulletW < enemyX[i]+enemyW-collision_offet:
                # collision
                state = False
                bulletX = playerX+playerW/2-bulletW/2
                bulletY = playerY-bulletH
                enemyX[i] = random.randint(1, window_width-enemyW-off_horz_e)
                enemyY[i] = random.randint(off_vert_e, 150)
                score += 10
                collisionSound = mixer.Sound('explosion.wav')
                collisionSound.play()
                # enemySpeed += 0.1
                # dy_enemy[i] += 0.1
                print(score)
            if bulletY < enemyY[i]+enemyH and bulletY > enemyY[i] and bulletX+collision_offet < enemyX[i]+enemyW and bulletX > enemyX[i]+collision_offet:
                state = False
                bulletX = playerX+playerW/2-bulletW/2
                bulletY = playerY-bulletH
                enemyX[i] = random.randint(1, window_width-enemyW-off_horz_e)
                enemyY[i] = random.randint(off_vert_e, 150)
                score += 10
                collisionSound = mixer.Sound('explosion.wav')
                collisionSound.play()
                # enemySpeed += 0.1
                # dy_enemy[i] += 0.1
                print(score)

    else:
        screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over : Score is {}'.format(score), True, (0, 255, 0), (0, 0, 255)) 
        textRect = text.get_rect() 
        textRect.center = (window_width // 2, window_height // 2)
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    showScore(textX, textY)
    pygame.display.update()
    

# quit functionality so that it doesn't get hanged
