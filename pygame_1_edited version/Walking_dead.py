#파이 게임 불러오기
import pygame
import random
import os #좀비 이미지를 랜덤으로 폴더에서 가져오기 위해
import pygame.mixer
import time

#게임 초기화
pygame.init()

#배경 음악 설정
bullet_sound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/shoot.mp3")  

#게임창 옵션 설정        
size = [400, 600]
screen = pygame.display.set_mode(size)

##게임 타이틀
title = "Walking Dead"
pygame.display.set_caption(title)

#게임 설정
clock = pygame.time.Clock()

zombie_images = ['zombie.png', 'zombie2.png','zombie3.png','zombie4.png']
heart_images = ["LeeFullHeart","LeeTwoLeftHeart","LeeOneLeftHeart"]
zombie_sounds = [
    "C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/zombie_sounds1.mp3",
    "C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/zombie_sounds2.mp3"
]
lastZombieSpawnTime = time.time()  # 이전 좀비가 생성된 시간을 저장
zombieSpawnTime = 0.2  # 좀비 생성 간격 

lastZombieSoundTime = time.time() #현 시간을 저장
zombieSoundsTime = 1.5 # 좀비 사운드간의 재생 시간 간격

#코드 내 이미지 활용 클래스
class PhotoShop:
    def __init__(self):
        self.x = 0
        self.y = 0
        #아래의 코드 없이 코드를 실행할 경우 캐릭터의 움직임이 매우 느리다.
        #때문에 다음의 코드를 추가로 작성해준다. 
        self.move = 1.2
         # 생명 이미지 추가
        self.life_images = [
            "C:/Users/ilove/Desktop/Games/pygame_1_edited version/heartImages/LeeFullHeart.png",
            "C:/Users/ilove/Desktop/Games/pygame_1_edited version/heartImages/LeeTwoLeftHeart.png",
            "C:/Users/ilove/Desktop/Games/pygame_1_edited version/heartImages/LeeOneLeftHeart.png"
        ]
        self.life_index = 0  # 초기 생명 이미지 인덱스
    def insertPhoto(self, address):
        self.image = pygame.image.load(address)
    
    def resizePhoto(self, xw, yh): #xw -> width, yh->height
        self.image = pygame.transform.scale(self.image, (xw, yh))
        self.xw, self.yh = self.image.get_size()
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        screen.blit(self.image, (self.x, self.y))
    

#총알 클래스
class Bullet(PhotoShop):
    def __init__(self, x, y):
        super().__init__()
        self.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1_edited version/images/bullet.png")
        self.resizePhoto(20, 20)
        self.x = x
        self.y = y
        self.move = random.uniform(0.1, 1)
def boom(a,b):
    if (a.x - b.xw <= b.x) and (b.x <= a.x +a.xw):
        if (a.y - b.yh <= b.y) and (b.y <= a.y + a.yh):
            return True
        else:
            return False
    else: 
        return False
    
#좀비 클래스
class Zombie(PhotoShop):
    def __init__(self):
        super().__init__()
        self.insertPhoto(os.path.join("C:/Users/ilove/Desktop/Games/pygame_1_edited version/zombieImages", random.choice(zombie_images)))
        self.resizePhoto(90, 90)
        self.x = random.randrange(0, size[0] - self.xw - round(self.xw / 2))
        self.y = 10
        self.move = 0.1
        self.zombie_sound = pygame.mixer.Sound(random.choice(zombie_sounds))  # 랜덤한 좀비 효과음 선택
         
##배경 설정
background = PhotoShop()
background.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1_edited version/images/game_background.png")
background.resizePhoto(size[0], size[1])
background.set_position(0, 0)

    
##등장인물 리-설정
Lee = PhotoShop()
Lee.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1_edited version/images/LeeWithGun.png") 
Lee.resizePhoto(120, 120)
Lee.set_position(round(size[0] / 2) - Lee.image.get_width() // 2, size[1] - Lee.image.get_height() - 15)

#인트로 화면 설정
black = (0, 0, 0)

#띄울 글자 설정
mainfont = pygame.font.Font("DungGeunMo.ttf", 25)
mainText= mainfont.render("KILL ZOMBIE!", True, (255, 255, 255))
subText = mainfont.render("PRESS SPACEBAR TO START", True, (255, 255, 255))

# 인트로 음악 설정
introBackgroundMusic = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/gameIntro.mp3")
intro = True
while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                intro = False
    
    #인트로 음악 재생
    introBackgroundMusic.play(-1)


    screen.fill(black)
    screen.blit(mainText, (120, round(size[1]/2 -50)))
    screen.blit(subText, (50, size[1] // 2 + 20))
    pygame.display.flip()
    
# 인트로 음악 중지
introBackgroundMusic.stop()

#배경 음악 재생을 인트로 음악 재생보다 앞에 뒀을 경우
#음악이 동시에 재생된다.
backgroundMusic = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/8-bit-arcade-138828.mp3")
backgroundMusic.play(-1) 

#메인 이벤트
WD = 0
moving_left = 0
moving_right = 0
moving_bullet = 0
k = 0
# 죽인 좀비와 실패한 좀비 수 초기화
killZombie = 0
lossZombie = 0

#좀비 리스트
zombieList = []
# 총알 리스트
bulletList = []

heartList = []

       
while WD == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WD = True #게임 종료    
        if event.type == pygame.KEYDOWN: #키 눌렀을 때
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                moving_bullet = True
                bullet_sound.play()
        elif event.type == pygame.KEYUP: # 키에서 손을 뗐을 때
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                moving_bullet = False
    
        
    #주인공의 이동, 화면 출력 설정              
    if moving_left:
        Lee.x -= Lee.move
        if Lee.x <= 0:
            Lee.x = 0
    elif moving_right:
        Lee.x += Lee.move
        if Lee.x >= size[0] - Lee.xw:
            Lee.x = size[0] - Lee.xw
   
    #총알의 이동과 화면 출력        
    if moving_bullet and k % 40 == 0:
        bullet = PhotoShop()
        bullet.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1_edited version/images/bullet.png")
        bullet.resizePhoto(20, 20)
        bullet.x = round(Lee.x + Lee.xw / 2 - bullet.xw / 2)
        bullet.y = Lee.y - 10 
        bullet.move = 1
        bulletList.append(bullet)
        
    k += 1
    
    # 총알 이동 및 화면에 그리기
    delBullet= []
    for Bullet in range(len(bulletList)):
        bL = bulletList[Bullet]
        bL.y -= bL.move
        if bL.y <- bL.yh:
            delBullet.append(Bullet)
    
    for dB in delBullet:
        del bulletList[dB]
   
    #좀비 등장
    currentTime = time.time()
    if random.random() > 0.99:
        if currentTime - lastZombieSoundTime >= zombieSoundsTime: #새로운 좀비의 생성 시간을 저장
            lastZombieSoundTime = currentTime
            zombie = PhotoShop()
            zombie.insertPhoto(os.path.join("C:/Users/ilove/Desktop/Games/pygame_1_edited version/zombieImages", random.choice(zombie_images)))
            zombie.resizePhoto(90, 90)
            zombie.x = random.randrange(0, size[0] - zombie.xw - round(zombie.xw / 2))
            zombie.y = 10
            zombie.move = 0.3
            zombie.zombie_sound = pygame.mixer.Sound(random.choice(zombie_sounds))  # 좀비 효과음 선택
            zombieList.append(zombie)
            zombie.zombie_sound.play() # 좀비 효과음 재생
        
    delZombie = []   
    for i in range(len(zombieList)):
        zom = zombieList[i]
        zom.y += zom.move
        if zom.y >= size[1]:
            delBullet.append(i)
    
    # 좀비 삭제
    for index in reversed(delZombie):
        zom = zombieList[index]
        zom.zombie_sound.stop()  # 해당 좀비의 사운드 중지
        del zombieList[index]
        
    #총알과 좀비의 충돌
    delbul = []
    delzom = []
    
    for i in range(len(bulletList)):
        for j in range(len(zombieList)):
            bL = bulletList[i]
            zom = zombieList[j]
            if boom(bL, zom) == True:
                delbul.append(i)
                delzom.append(j)
                killZombie += 1  # 좀비를 죽였을 때 kill 1 증가
                
    #중복 제거
    delbul = list(set(delbul))
    delzom = list(set(delzom))
    
    for dB in delbul:
        del bulletList[dB]
    for zom in delzom:
        if zom < len(zombieList):
            del zombieList[zom]
    
    for i in range(len(zombieList)):
        zom = zombieList[i]
        if boom (zom, Lee) == True:
            WD = 1
    
     # 좀비 삭제
    delZombie = []
    for i in range(len(zombieList)):
        zom = zombieList[i]
        zom.y += zom.move
        if zom.y >= size[1]:
            delZombie.append(i)
            lossZombie += 1  # 좀비를 죽이지 못했을 때 loss 1 증가

    for index in reversed(delZombie):
        zom = zombieList[index]
        zom.zombie_sound.stop()  # 해당 좀비의 사운드 중지
        del zombieList[index]
    
    background.show()
    
    for heart in heartList:
        heart.show()
        
    Lee.show()
    
    for bL in bulletList:
        bL.show()
    for zom in zombieList:
        zom.show()
    
     # 글자 띄우기
    font = pygame.font.Font("DungGeunMo.ttf", 25)
    textKillLoss = font.render("Kill: {} Loss: {}".format(killZombie, lossZombie), True, (255,0,0))
    screen.blit(textKillLoss, (10, 5))
 
     
    pygame.display.flip()  
    
    
   # 게임 종료 멘트 폰트 설정
end_font = pygame.font.Font("DungGeunMo.ttf", 30)
end_text = end_font.render("You Killed By Zombie", True, (255, 0, 0))
end_sub_text = end_font.render("Press any key to exit", True, (255, 0, 0))
# 오디오 초기화
pygame.mixer.init()

# 게임 종료 음악 설정
gameOverMusic = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1_edited version/music/gameOver.mp3")

# 게임 종료 음악 재생
gameOverMusic.play()

# 게임 배경 음악 중지
backgroundMusic.stop()

# 게임 종료 화면 루프
game_over = True
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            exit() 
    
    screen.fill((0, 0, 0))
    screen.blit(end_text, (size[0] // 2 - end_text.get_width() // 2, size[1] // 2 - 20))
    screen.blit(end_sub_text, (size[0] // 2 - end_sub_text.get_width() // 2, size[1] // 2 + 20))
    pygame.display.flip()

pygame.quit() #게임 끄기
