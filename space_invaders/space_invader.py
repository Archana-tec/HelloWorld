import pygame, time
import random
import math


# Initialise the pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#background music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# player
Playerimg = pygame.image.load("player.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
#
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "Ready"

#score
score_value= 0
font = pygame.font.Font(("freesansbold.ttf"), 32)
over_font = pygame.font.Font(("freesansbold.ttf"), 64)

textX = 10
textY =10

def show_score(x,y):
    score = font.render("Score: "+str(score_value), True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_font = font.render("Game Over: "+str(score_value), True,(255,255,255))
    screen.blit(over_font,(300,250))



# def functions
def player(x, y):
    screen.blit(Playerimg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))
    pygame.display.update()


def collision(bulletX, bulletY, enemyX, enemyY):
    Distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if Distance < 27:
        return True
    else:
        return False


Running = True
while Running:
    screen.fill((0, 0, 255))
    screen.blit(pygame.image.load('background.png'), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        # checking keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -10
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = PlayerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("keystroke released")
                PlayerX_change = 0

    # Bullet movement
    if bulletY < 0:
        bullet_state = "Ready"
        bulletY = 480
    if bullet_state == "Fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #collision



    PlayerX += PlayerX_change
    if PlayerX < 0:
        PlayerX = 0
    if PlayerX > 736:
        PlayerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] >400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i]= 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        Collision = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if Collision:
            explosion_sound = pygame.mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

    player(PlayerX, PlayerY)
    show_score(textX,textY)
    pygame.display.update()


