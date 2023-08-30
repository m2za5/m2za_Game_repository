#파이 게임 불러오기
import pygame
import random
import os #좀비 이미지를 랜덤으로 폴더에서 가져오기 위해
import pygame.mixer

#게임 초기화
pygame.init()

backgroundMusic = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1/music/8-bit-arcade-138828.mp3")
backgroundMusic.play(-1) 
bullet_sound = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/pygame_1/music/shoot.mp3")  
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
            "C:/Users/ilove/Desktop/Games/pygame_1/heartImages/LeeFullHeart.png",
            "C:/Users/ilove/Desktop/Games/pygame_1/heartImages/LeeTwoLeftHeart.png",
            "C:/Users/ilove/Desktop/Games/pygame_1/heartImages/LeeOneLeftHeart.png"
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
        self.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1/images/bullet.png")
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

         
##배경 설정
background = PhotoShop()
background.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1/images/game_background.png")
background.resizePhoto(size[0], size[1])
background.set_position(0, 0)

    
##등장인물 리-설정
Lee = PhotoShop()
Lee.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1/images/LeeWithGun.png") 
Lee.resizePhoto(120, 120)
Lee.set_position(round(size[0] / 2) - Lee.image.get_width() // 2, size[1] - Lee.image.get_height() - 15)



#메인 이벤트
WD = 0
moving_left = 0
moving_right = 0
moving_bullet = 0
k = 0
player_life = 3

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
        bullet.insertPhoto("C:/Users/ilove/Desktop/Games/pygame_1/images/bullet.png")
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
    if random.random() > 0.99:
        zombie = PhotoShop()
        zombie.insertPhoto(os.path.join("C:/Users/ilove/Desktop/Games/pygame_1/zombieImages", random.choice(zombie_images)))
        zombie.resizePhoto(90, 90)
        zombie.x = random.randrange(0, size[0] - zombie.xw - round(zombie.xw / 2))
        zombie.y = 10
        zombie.move = 0.1
        zombieList.append(zombie)
    
    for i in range(len(zombieList)):
        zom = zombieList[i]
        zom.y += zom.move
        if zom.y >= size[1]:
            delBullet.append
    
    delZombie = []
    for dB in delZombie:
        del zombieList[dB]
        
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
    
    
    #중복 제거
    delbul = list(set(delbul))
    delzom = list(set(delzom))
    
    for dB in delbul:
        del bulletList[dB]
    for zom in delzom:
        del zombieList[zom]
    
    for i in range(len(zombieList)):
        zom = zombieList[i]
        if boom (zom, Lee) == True:
            WD = 1
    
    
    background.show()
    
    for heart in heartList:
        heart.show()
        
    Lee.show()
    
    for bL in bulletList:
        bL.show()
    for zom in zombieList:
        zom.show()
     
     
    pygame.display.flip()  

pygame.quit() #게임 끄기