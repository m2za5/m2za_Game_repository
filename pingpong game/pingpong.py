import pygame
import sys
from pygame.locals import *

#사운드 설정
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)
ballSound = pygame.mixer.Sound('pop.mp3')

startGame = True  # 게임 루프를 제어할 변수

# 초기화 함수
def init():
    global startGame  # startGame을 전역 변수로 사용합니다.
    pygame.init()
    screen_width = 890
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BLOCK GAME")
    font = pygame.font.SysFont("DungGeunMo", 100)
    gameOvertext = font.render("GAME OVER!", True, (255, 255, 255))
    gameOvertextRect = gameOvertext.get_rect()  # textRect를 gameOvertext에 대한 Rect로 설정
    gameOvertextRect.center = (screen_width // 2, screen_height // 2)  # 화면 중앙에 배치

    retry_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 50, 100, 40)
    pygame.draw.rect(screen, (0, 255, 0), retry_button)
    font = pygame.font.Font(None, 36)
    text = font.render("Retry", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = retry_button.center

    screen.blit(gameOvertext, gameOvertextRect)
    screen.blit(text, textRect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 'QUIT' 이벤트를 확인합니다.
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    startGame = True  # Retry 버튼을 클릭하면 startGame을 다시 True로 설정하여 게임을 다시 시작
                    return
    
def block_init(blockList1, blockList2, blockList3, blockList4, blockList5, blockList6, blockList7):
    x = 20
    y = 10
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList1.append(blcokObject)
        x += 85
    x = 20
    y += 35
    
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList2.append(blcokObject)
        x += 85
    x = 20
    y += 35
       
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList3.append(blcokObject)
        x += 85
    x = 20
    y += 35
        
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList4.append(blcokObject)
        x += 85
    x = 20
    y += 35
        
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList5.append(blcokObject)
        x += 85   
    x = 20
    y += 35
    
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList6.append(blcokObject)
        x += 85   
    x = 20
    y += 35
    
    for i in range(10):
        blcokObject = pygame.Rect(x, y, 80, 30)
        blockList7.append(blcokObject)
        x += 85   
    x = 20
    y += 35
        

def mainGame():
    global startGame
    pygame.init()
    screenWidth = 890
    screenHeight = 700
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("PingPong 게임")
    
    clock = pygame.time.Clock()
    gameSpeed = 0.8

    vel = [-0.4, -0.4] # x축과 y축의 속도, 대각선으로 이동

    
    
    barObject = pygame.Rect((screenWidth - 200) / 2, 600, 200, 400)
    barPic = pygame.image.load("bar.png")
    barPic = pygame.transform.scale(barPic, (200, 40))
    
    
    ballObject = pygame.Rect((screenWidth - 40)/2, (screenHeight - 40)/2, 40, 40)
    ballPic = pygame.image.load("ball.png")
    ballPic = pygame.transform.scale(ballPic, (40, 40))
    
    
    #벽돌 리스트
    listOfBlock1 = []
    listOfBlock2 = []
    listOfBlock3 = []
    listOfBlock4 = []
    listOfBlock5 = []
    listOfBlock6 = []
    listOfBlock7 = []

    #벽돌 색
    blockColor = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
    block_init(listOfBlock1, listOfBlock2, listOfBlock3, listOfBlock4, listOfBlock5, listOfBlock6, listOfBlock7)
    
    while startGame:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 'QUIT' 이벤트를 확인합니다.
                pygame.quit()
                sys.exit()
        if startGame:
            KeyInput = pygame.key.get_pressed()
            if KeyInput[K_LEFT] and barObject.left >= 0:
                barObject.left -= gameSpeed * dt
            if KeyInput[K_RIGHT] and barObject.right <= screenWidth:
                barObject.right += gameSpeed * dt
            
            
            ballObject.x += vel[0] * dt
            ballObject.y += vel[1] * dt   
            
            if ballObject.left <= 0 or ballObject.right >= screenWidth:
                vel[0] *= -1
            if ballObject.top <= 0:
                vel[1] *= -1
                
            #공이 바닥에 떨어졌을 때
            if ballObject.bottom >= screenHeight:
                return init()
            
            #공과 바의 충돌
            if ballObject.colliderect(barObject):
                ballSound.play()
                ballObject.bottom = barObject.top  # 공이 바와 충돌한 후에 튕기도록 수정
                vel[1] *= -1
                
                
        screen.fill((255, 255, 255))
        
        #바 그리기
        screen.blit(barPic, barObject)
        
        # 공 그리기
        screen.blit(ballPic, ballObject)
        
        
        for block in listOfBlock1:
            pygame.draw.rect(screen, blockColor[0], block)
        for block in listOfBlock2:
            pygame.draw.rect(screen, blockColor[1], block)
        for block in listOfBlock3:
            pygame.draw.rect(screen, blockColor[2], block)
        for block in listOfBlock4:
            pygame.draw.rect(screen, blockColor[3], block)
        for block in listOfBlock5:
            pygame.draw.rect(screen, blockColor[4], block)
        for block in listOfBlock6:
            pygame.draw.rect(screen, blockColor[5], block) 
        for block in listOfBlock7:
            pygame.draw.rect(screen, blockColor[6], block)    
            
        #공과 블럭의 충돌
        for block in listOfBlock1:
            if ballObject.colliderect(block):
                listOfBlock1.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock2:
            if ballObject.colliderect(block):
                listOfBlock2.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock3:
            if ballObject.colliderect(block):
                listOfBlock3.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock4:
            if ballObject.colliderect(block):
                listOfBlock4.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock5:
            if ballObject.colliderect(block):
                listOfBlock5.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock6:
            if ballObject.colliderect(block):
                listOfBlock6.remove(block)
                vel[1] *= -1
                
        for block in listOfBlock7:
            if ballObject.colliderect(block):
                listOfBlock7.remove(block)
                vel[1] *= -1
                
        pygame.display.update()

while True:
    if startGame:  # 초기화 함수 호출
        mainGame()
