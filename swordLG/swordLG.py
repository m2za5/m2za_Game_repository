import pygame
from pygame import mixer
from character import Character
import sys

pygame.init()

# screen
screenWidth = 1200
screenHeight = 650

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sword Warriors")

# Intro music
pygame.mixer.music.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/Music/IntroMusic.WAV")

# intro image
introImage = [
    pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/IntroImage/Elegy.png"),
    pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/IntroImage/Aqueducts Of Tears.png"),
    pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/IntroImage/Beams Of Hope.png"),
    pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/IntroImage/After The Flood.png")
]

# intro text
introText = [
    [
        "One day, the world came to an end.",
        "Many people were killed or injured because it happened suddenly.",
        "The government abandoned the people."
    ],
    [
        "People have been hiding somewhere to live.",
        "The world with nothing left was calm and beautiful."
    ],
    [
        "But somewhere, a man who called himself a hero appeared",
        "and started fighting to rebuild the world.",
        "He fought, willing to give up his life and disappeared.",
    ],
    [
        "People came out of the world again and began to rebuild the collapsed world.",
        "The world searched for him, but in the end people couldn't find him.",
        "The sound of him fighting for the world is still echoing somewhere."
    ]
]

#narration
font = pygame.font.Font("C:/Users/ilove/Desktop/Games/remaster_swordLG/Font/DungGeunMo.ttf", 30)
introTextColor = (255, 0, 0)

# Image scale def
def scale_image(image, target_width, target_height):
    return pygame.transform.scale(image, (target_width, target_height))

# loop
intro_done = False
current_index = 0
clock = pygame.time.Clock()

pygame.mixer.music.play(-1)

while not intro_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # if player presses enter... show next image
                current_index += 1
                if current_index >= len(introImage):
                    intro_done = True

    screen.fill((0, 0, 0))
    if current_index < len(introImage):
        # how images after scale
        scaled_image = scale_image(introImage[current_index], screenWidth, screenHeight)
        screen.blit(scaled_image, (0, 0))

    # when len(index) < len(text List)
    if current_index < len(introText):
        y_offset = 0
        for line in introText[current_index]:
            text_surface = font.render(line, True, introTextColor)
            text_rect = text_surface.get_rect(center=(screenWidth // 2, screenHeight - 80 + y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_rect.height 

    pygame.display.flip()
    clock.tick(60)

screen.fill((0, 0, 0))
pygame.display.flip()

#  game introduce
intro_done = False
intro_text = [
   "This game is for two people.",
   " ",
   "Swordsman: Move [W, A, S, D]",
   "Press [W, A, S, D] and press L-shift at the same time to dash",
   "Attack with [R, T]",
   " ",
   " ",
   "Samurai: Move [Arrow keys]",
   "Press the [Arrow keys] and press the R-shift at the sam time to dash",
   "Attack with [K, L]"
   " ",
   " ",
   "PRESS ENTER TO START."
]
y_offset = 0
for line in intro_text:
    text_surface = font.render(line, True, introTextColor)
    text_rect = text_surface.get_rect(center=(screenWidth // 2, screenHeight - 500 + y_offset))
    screen.blit(text_surface, text_rect)
    y_offset += text_rect.height
pygame.display.flip()

while not intro_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  #if player presses enter... show game
                intro_done = True
                
                
pygame.mixer.music.stop()

  
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
pygame.mixer.music.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/Music/backgroundMusic.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0, 5000)

#when round is over
nextFightSound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/nextFight.mp3")
nextFightSound.set_volume(0.5)

getReady = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/fight.mp3")
getReady.set_volume(0.4)

#sound of characters
swordPlayer = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/EnemySword.mp3")
swordPlayer.set_volume(0.6)

swordEnemy = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/PlayerSword.mp3")
swordEnemy.set_volume(0.8)

PlayerHurt = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/PlayerHurt.mp3")
PlayerHurt.set_volume(0.6)

EnemyHurt = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/remaster_swordLG/SoundEffect/EnemyHurt.mp3")
EnemyHurt.set_volume(0.6)


#background
background = pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/Background/background.png")


#load character
PlayerCharacter = pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/Player/Player.png").convert_alpha()
EnemyCharacter = pygame.image.load("C:/Users/ilove/Desktop/Games/remaster_swordLG/image/Enemy/Enemy.png").convert_alpha()

#animation
PlayerAnimation = [8, 4, 4, 8, 2, 3, 3, 7]
EnemyAnimation = [8, 8, 2, 6, 6, 2, 4, 6]

#font
countFont = pygame.font.Font("C:/Users/ilove/Desktop/Games/remaster_swordLG/Font/DungGeunMo.ttf", 80)
scoreFont = pygame.font.Font("C:/Users/ilove/Desktop/Games/remaster_swordLG/Font/DungGeunMo.ttf", 40)

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
    drawText("Swordsman:" + str(score[0]), scoreFont, RED, 30, 60)
    drawText("Samurai:" + str(score[1]), scoreFont, RED, 770, 60)
    
    
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
            getReady.play()
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
        if not nextFightSound:
            # Play applause sound effect only once
            nextFightSound.play()
            nextFightSound = True
        
        if pygame.time.get_ticks() - roundOverTime > 2000:
            # Play applause sound effect
            nextFightSound.stop()
            
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