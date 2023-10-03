import pygame

class Character():
    def __init__(self, player, x, y, flip, data, spriteSheet, animationSteps, sound, hurtSound):
        self.player = player
        self.size = data[0]
        self.imageScale = data[1]
        self.offset = data[2]
        self.filp = flip
        self.animationList = self.loadImages(spriteSheet, animationSteps)
        self.action = 0 #0 = idle, 1 = attack1 , 2 = attack2, 3 = run, 4 = jump, 5 = fall ,6 = attaked, 7 = death
        self.framIndex = 0
        self.image = self.animationList[self.action][self.framIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y, 80, 180))
        self.velY = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attackType = 0
        self.attackCooldown = 0
        self.attackSound = sound
        self.hurtSound = hurtSound
        self.hit = False
        self.health = 100
        self.alive = True
    
    def loadImages(self, spriteSheets, animationSteps):
        #extract images
        animationList = []
        for y, animation in enumerate(animationSteps):      
            tempImgList = []
            for x in range(animation):
                tempImg = spriteSheets.subsurface(x * self.size, y * self.size, self.size, self.size)
                tempImgList.append(pygame.transform.scale(tempImg, (self.size * self.imageScale, self.size * self.imageScale)))
            animationList.append(tempImgList)
        return animationList
        
    
    def move(self, screen_width, screen_height, surface, enemy, round_Over):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attackType = 0
        
        #get key
        key = pygame.key.get_pressed()
        
        if self.attacking == False and self.alive == True and round_Over == False:
            #check Player control
            if self.player == 1:    
                #movement
                if key[pygame.K_a]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.velY = -30
                    self.jump = True
                    
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(enemy)
                    #which attack type
                    if key[pygame.K_r]:
                        self.attackType = 1
                    if key[pygame.K_t]:
                        self.attackType = 2 
                        
                        
              #check Enemy control
            if self.player == 2 and self.alive == True:    
                #movement
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.velY = -30
                    self.jump = True
                    
                #attack
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.attack(enemy)
                    #which attack type
                    if key[pygame.K_k]:
                        self.attackType = 1
                    if key[pygame.K_l]:
                        self.attackType = 2 
            
        #gravity
        self.velY += gravity   
        dy += self.velY
        
        #stay screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.velY = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
            
        #face each other
        if enemy.rect.centerx > self.rect.centerx:
            self.filp = False
        else:
            self.filp = True
            
        
        #attackCooldown
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
            
        #position of player    
        self.rect.x += dx
        self.rect.y += dy
        
        
    #animation update    
    def update(self):
        #check what charcter's action
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.updatAction(7)
        elif self.hit == True:
            self.updatAction(6)
        elif self.attacking:
            if self.attackType == 1:
                self.updatAction(1)
            elif self.attackType == 2:
                self.updatAction(2)
        elif self.jump == True:
            self.updatAction(4)
        elif self.running == True:
            self.updatAction(3)
        else:
            self.updatAction (0)
        
        animationCooldown = 90
        self.image = self.animationList[self.action][self.framIndex]
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.framIndex += 1
            self.updateTime = pygame.time.get_ticks()
        if self.framIndex >= len(self.animationList[self.action]):
            #check player dead and end anomation
            if self.alive == False:
                self.framIndex = len(self.animationList[self.action]) - 1
            else:
                self.framIndex = 0
                #finish attacking
                if self.action == 1 or self.action == 2:
                    self.attacking = False
                    self.attackCooldown = 20
                #check damage
                if self.action == 6:
                    self.hit = False
                    self.attacking = False
                    self.attackCooldown = 20
            
        
    def attack(self,  enemy):
        if self.attackCooldown == 0:
            self.attacking = True
            self.attackSound.play()
            attackingRect = pygame.Rect(self.rect.centerx - ( 2 * self.rect.width * self.filp) ,self.rect.y, 2 * self.rect.width, self.rect.height)
            if attackingRect.colliderect(enemy.rect):
                enemy.health -= 10
                enemy.hit = True
                enemy.hurtSound.play()
   
   
    def updatAction(self, newAction):
        #check different action
        if newAction != self.action:
            self.action = newAction
            #update animation
            self.framIndex = 0
            self.updateTime = pygame.time.get_ticks()
        
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.filp, False)
        surface.blit(img, (self.rect.x- (self.offset[0] * self.imageScale), self.rect.y - (self.offset[1] * self.imageScale)))