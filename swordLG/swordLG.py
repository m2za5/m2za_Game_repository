import pygame
from pygame import mixer
from character import Character

mixer.init()
pygame.init()


# 화면 생성
screenWidth = 1200
screenHeight = 650

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sword")

#set Frame
clock = pygame.time.Clock()
frameSpeed = 60

#define color
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game vairable
introCount = 3
lastCountUpdate = pygame.time.get_ticks()
score = [0, 0] #chracter score player and enemy
roundOver = False
roundOverCoolDown = 2000

#player variable
PlayerSize = 200
PlayerScale = 3
PlayerOffset = [89, 72]
PlayerData = [PlayerSize, PlayerScale, PlayerOffset]
EnemySize = 200
EnemyScale = 3
EnemyOffset = [86, 67]
EnemyData = [EnemySize, EnemyScale, EnemyOffset]

#music and sound
pygame.mixer.music.load("C:/Users/ilove/Desktop/Games/swordLG/Battle.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0, 5000)


#applause sound
applauseSound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/applausesound.mp3")
applauseSound.set_volume(0.3)

#let's fight!...
fightSound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/fight!.mp3")
fightSound.set_volume(0.6)

nextFightSound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/nextFight.mp3")
nextFightSound.set_volume(0.6)


#sound of characters
swordPlayer = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/EnemySword.mp3")
swordPlayer.set_volume(0.6)

swordEnemy = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/PlayerSword.mp3")
swordEnemy.set_volume(1)

PlayerHurt = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/PlayerHurt.mp3")
PlayerHurt.set_volume(0.6)

EnemyHurt = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/swordLG/SoundEffect/EnemyHurt.mp3")
EnemyHurt.set_volume(0.6)


#background
background = pygame.image.load("C:/Users/ilove/Desktop/Games/swordLG/image/Background/Battleground1.png")

# You Win!
winner = pygame.image.load("C:/Users/ilove/Desktop/Games/swordLG/image/Win/You win!.png").convert_alpha()


#load character
PlayerCharacter = pygame.image.load("C:/Users/ilove/Desktop/Games/swordLG/image/Player/Player.png").convert_alpha()
EnemyCharacter = pygame.image.load("C:/Users/ilove/Desktop/Games/swordLG/image/Enemy/Enemy.png").convert_alpha()

#animation
PlayerAnimation = [8, 4, 4, 8, 2, 3, 3, 7]
EnemyAnimation = [8, 8, 2, 6, 6, 2, 4, 6]

#font
countFont = pygame.font.Font("C:/Users/ilove/Desktop/Games/swordLG/Font/DungGeunMo.ttf", 80)
scoreFont = pygame.font.Font("C:/Users/ilove/Desktop/Games/swordLG/Font/DungGeunMo.ttf", 40)

#draw text
def drawText(text, font, textColor, x, y):
    fontImg = font.render(text, True, textColor)
    screen.blit(fontImg,(x, y))

#draw backgrounds
def drawBackground():
    scaleBackground = pygame.transform.scale(background,(screenWidth, screenHeight))
    screen.blit(scaleBackground, (0, 0))

#health bar
def drawHealthBar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    
#draw characters
Player = Character(1, 200, 360,False, PlayerData, PlayerCharacter, PlayerAnimation, swordEnemy, PlayerHurt)
Enemy = Character(2, 900, 360, True, EnemyData, EnemyCharacter, EnemyAnimation, swordPlayer, EnemyHurt)


#game loop
runningGame = True
while runningGame:
    
    clock.tick(frameSpeed)
    
    #draw background
    drawBackground()
    
    #draw health
    drawHealthBar(Player.health, 30, 20)
    drawHealthBar(Enemy.health, 770, 20)
    drawText("Player1:" + str(score[0]), scoreFont, RED, 30, 60)
    drawText("Player2:" + str(score[1]), scoreFont, RED, 770, 60)
    
    
    #print intro character
    if introCount < 0 :
        #move character
        Player.move(screenWidth, screenHeight, screen, Enemy, roundOver)
        Enemy.move(screenWidth, screenHeight, screen, Player, roundOver)
    else:
        #show text
        drawText(str(introCount), countFont, RED, screenWidth / 2 , screenHeight / 3)
         # Play countdown sound effect
        if introCount == 3:
            fightSound.play()
        #update timer
        if pygame.time.get_ticks() - lastCountUpdate >= 1000:
            introCount -= 1
            lastCountUpdate = pygame.time.get_ticks()
        
    
    #update  characters
    Player.update()
    Enemy.update()
    
    #draw character
    Player.draw(screen)
    Enemy.draw(screen)
    
    
    #who defeat
    if roundOver == False:
        if Player.alive == False:
            score[1] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()
        elif Enemy.alive == False:
            score[0] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()
    else:
        #show winner
        screen.blit(winner, (380, 200))
        if pygame.time.get_ticks() - roundOverTime <= 2000:
            # Play applause sound effect
            applauseSound.play()
            
        if pygame.time.get_ticks() - roundOverTime > roundOverCoolDown:
            nextFightSound.play()
            roundOver = False
            introCount = 3
            Player = Character(1, 200, 360,False, PlayerData, PlayerCharacter, PlayerAnimation, swordEnemy, PlayerHurt)
            Enemy = Character(2, 900, 360, True, EnemyData, EnemyCharacter, EnemyAnimation, swordPlayer, EnemyHurt)
    
    #event handeler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningGame = False
    
    #update display
    pygame.display.update()           
#exit game
pygame.quit()