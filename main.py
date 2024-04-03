import pygame
import random

# screen constants
HEIGHT = 600
WIDTH = 800

# player constants
PLAYERSIZE = 64
PRIGHTBOUND = WIDTH-PLAYERSIZE
PLEFTBOUND = 0
PSPEED = 3

# enemy constants
ENEMYSIZE = 64
ERIGHTBOUND = WIDTH-ENEMYSIZE
ELEFTBOUND = 0
EUPBOUND = 0
EDOWNBOUND = HEIGHT/2 - ENEMYSIZE/2
EXSPEED = 1
EYSPEED = 0.5
ENEMYFREQ = 300

# fire constants
FIRESIZE = 16
FSPEED = 1
FIRESTARTPOS = PLAYERSIZE/2 - FIRESIZE/2

# explosion constants
EXPLOSIONSIZE = 32
EXPLOSIONTIMEOUT = 50
EXPLOSIONPOS = ENEMYSIZE/2 - EXPLOSIONSIZE/2

# initialise pygame
pygame.init()

# creating screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icons/playericon.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('icons/background.jpg')

# sounds
pygame.mixer.music.load('sounds/bgsound.mp3')
firesound = pygame.mixer.Sound('sounds/firesound.mp3')
explosionsound = pygame.mixer.Sound('sounds/explosionsound.mp3')
gameoversound = pygame.mixer.Sound('sounds/gameoversound.mp3')
pygame.mixer.music.play(-1)

# player init
playerIcon = pygame.image.load('icons/playericon.png')
playerX = WIDTH/2 - PLAYERSIZE/2
playerY = 5*HEIGHT/6


# enemy init
class Enemy():
    def __init__(self, score):
        self.enemyIcon = pygame.image.load(f'icons/enemyicon{score}.png')
        self.enemyX = random.randint(ELEFTBOUND, ERIGHTBOUND)
        self.enemyY = random.randint(EUPBOUND, EDOWNBOUND)
        self.score = 5 if score < 2 else 10

    def move(self):
        enemyXchange = 0
        if self.enemyX <= ELEFTBOUND:
            enemyXchange = EXSPEED
        if self.enemyX >= ERIGHTBOUND:
            enemyXchange = -EXSPEED
        self.enemyX += enemyXchange
        self.enemyY += EYSPEED
        screen.blit(self.enemyIcon, (self.enemyX, self.enemyY))


# fire init
class Fire():
    def __init__(self, fireX):
        self.fireIcon = pygame.image.load('icons/fire.png')
        self.fireX = fireX
        self.fireY = playerY - FIRESIZE

    def fire(self):
        screen.blit(self.fireIcon, (self.fireX, self.fireY))
        self.fireY -= FSPEED


# explosion
explosion = pygame.image.load('icons/explosion.png')
explodeX = -1
explodeY = -1


def explode(x, y):
    screen.blit(explosion, (x+EXPLOSIONPOS, y+EXPLOSIONPOS))


# kill enemies
def kill(fireX, fireY, enemyX, enemyY):
    return fireY >= enemyY and fireY <= enemyY + ENEMYSIZE and fireX >= enemyX and fireX <= enemyX + ENEMYSIZE

# get killed by enemies


def killed(enemyX, enemyY):
    return playerY <= enemyY + ENEMYSIZE/2 and playerY >= enemyY and playerX >= enemyX - ENEMYSIZE and playerX <= enemyX + ENEMYSIZE


# game attributes
running = True
fires = []
enemies = []
timeToCreateEnemy = ENEMYFREQ
score = 0
curExplosion = 0
gameOverTimeOut = 300


# display score
scoreFont = pygame.font.SysFont('mono', 24)


def show_score():
    scoreText = scoreFont.render(
        "Score : " + str(score), True, (255, 255, 255))
    screen.blit(scoreText, (10, 5))


# display game over text
gameOverFont = pygame.font.SysFont('mono', 64)
skull = pygame.image.load('icons/skull.png')


def gameover():
    gameOverText = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOverText, (WIDTH/2 - (5*32), HEIGHT/2-32))


while running or gameOverTimeOut:

    # background fill
    screen.fill((0, 13, 26))
    screen.blit(background, (0, 0))

    # show score text
    show_score()

    if running:
        # draw player
        screen.blit(playerIcon, (playerX, playerY))

        # create enemy
        if timeToCreateEnemy == ENEMYFREQ:
            enemies.append(Enemy(random.randint(0, 2)))
            timeToCreateEnemy = 0

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gameOverTimeOut = 0

            # create fire
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    fires.append(Fire(playerX + FIRESTARTPOS))
                    firesound.play()

        # player movement
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and playerX > PLEFTBOUND:
            playerX -= PSPEED
        if keys_pressed[pygame.K_RIGHT] and playerX < PRIGHTBOUND:
            playerX += PSPEED

        # enemy movement
        for e in enemies:
            e.move()
            if killed(e.enemyX, e.enemyY):
                gameoversound.play()
                pygame.mixer.music.stop()
                running = False

        # fire movement
        remFires = []
        remEnemies = []
        for i in range(len(fires)):
            if fires[i].fireY <= 0:
                remFires.append(i)
            else:
                fires[i].fire()
                # fire kills enemies
                for j in range(len(enemies)):
                    if kill(fires[i].fireX, fires[i].fireY, enemies[j].enemyX, enemies[j].enemyY):
                        explodeX, explodeY = enemies[j].enemyX, enemies[j].enemyY
                        curExplosion = EXPLOSIONTIMEOUT
                        explosionsound.play()
                        remEnemies.append(j)
                        remFires.append(i)
                        score += enemies[j].score

        # remove off-enemies and off-fires
        for i in remEnemies:
            del enemies[i]
        for i in remFires:
            del fires[i]

        # explosion occurs
        if curExplosion:
            explode(explodeX, explodeY)
            curExplosion -= 1

        timeToCreateEnemy += 1

    else:
        gameOverTimeOut -= 1
        # draw skull
        screen.blit(skull, (playerX, playerY))
        # show game over text
        gameover()

    pygame.display.update()
