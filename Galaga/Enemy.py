from Bullets import Bullets, EnemyBullet 
import pygame, math, random

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, wave, spawnOrder, spawnSide, flightPattern, 
                    screenWidth, screenHeight):
        super().__init__() 
        (self.targetX1, self.targetY1, self.targetX2, self.targetY2,
            self.targetX3, self.targetY3) = flightPattern
        self.spawnOrder = spawnOrder
        self.spawnSide = spawnSide
        self.wave = wave 
        self.normalX, self.normalY = x, y
        self.screenWidth, self.screenHeight = screenWidth, screenHeight
        self.boss = False
        
        # image related init
        if self.wave % 2 == 0:
            self.img1 = pygame.transform.scale(pygame.image.load(
                        "Images/Enemy1.png"), (20, 25)).convert_alpha()
            self.img2 = pygame.transform.scale(pygame.image.load(
                        "Images/Enemy1B.png"), (30, 25)).convert_alpha()
        else:
            self.img1 = pygame.transform.scale(pygame.image.load(
                        "Images/Enemy2.png"), (20, 25)).convert_alpha()
            self.img2 = pygame.transform.scale(pygame.image.load(
                        "Images/Enemy2B.png"), (30, 25)).convert_alpha()
        self.baseImg1 = self.img1.copy()
        self.baseImg2 = self.img2.copy()
        self.frames = [self.baseImg1, self.baseImg2] 
        self.frame = 0
        self.image = self.frames[self.frame] 
        self.width, self.height = self.image.get_size()
        
        if self.spawnSide == "left":
            self.x = (0 - self.spawnOrder * (2* self.height))
            self.v = (self.targetX1) // 30
            self.angle = -90
        else: # spawn on right side of screen
            self.x = (self.screenWidth + self.spawnOrder * (2 * self.height))
            self.v = (self.targetX1 - self.screenWidth) // 30
            self.angle = 90 
        self.y = self.targetY1 + self.height//2  
        self.rotateImgs(self.angle)

        # motion related init
        self.vX = self.v 
        self.vY = 0
        self.boundLeft, self.boundRight = 0,0 #for dive only 
        self.timer = 0
        self.spawning = True 
        self.movingToNormal, self.mTNUpdates = False, 0
        self.normal = False
        self.dive =  False
        self.shoot = False
        self.bound = (self.wave + 1) * 5
        self.bounce = True 
        self.updateRect()

        if self.spawnOrder == 0:
            if self.spawnSide == "right":
                pass
                # print ("(%d %d), (%d %d), (%d %d)" % (self.targetX1,
                #  self.targetY1, self.targetX2,
                #  self.targetY2, self.targetX3, self.targetY3))
                 
            # print ("Enemy Wave:", self.wave)
            # print ("    Target 1  :", self.targetX1, self.targetY1)
            # print ("    Target 2  :",self.targetX2, self.targetY2)
        
    def update(self):
        if self.timer % 15 == 1: 
            self.animate()
        if self.timer % 20 == 1: # creates flapping that is semi-random
            self.animate()
        self.checkDive() 
        self.checkTargets() 
        
        if self.dive:
           self.diveBounds()
        elif self.movingToNormal:
            self.updateMoveToNormalVelocity()
            self.checkNormalMotion()    
        elif self.normal: 
            self.normalBounds() 
        
        self.x += self.vX
        self.y += self.vY 
        self.checkKill()
        self.updateRect()
        if self.spawnSide == "right":
            if self.spawnOrder == 0 and self.timer % 1 == 0:
                pass
                # print ("Curent Pos:", self.x, self.y)
        self.timer += 1
        
######## Motion Helper Functions ########
    
    def checkKill(self):
        if self.spawnSide == "left":
            if self.x > self.screenWidth: 
                self.kill()
        else:
            if self.x < 0: 
                self.kill()
        if self.y > self.screenHeight + self.height + 10: 
            self.kill()
            
    def checkTargets(self): 
        if not self.spawning: return 
        self.checkTarget1()
        self.checkTarget2()
        self.checkTarget3()
    
    def checkTarget1(self):
        if self.vX != 0: # simple way to prevent infinite loop
            if (self.rect.collidepoint(self.targetX1, self.targetY1)):
                self.x, self.y = self.targetX1, self.targetY1
                self.vX = 0
                self.vY = self.v
                if self.spawnSide == "left":
                    self.rotateImgs(-90)
                else: # right
                    self.vY = -self.vY
                    self.rotateImgs(90)
                self.animate()
    
    def checkTarget2(self):
        if self.vX == 0:
            if (self.rect.collidepoint(self.targetX2, self.targetY2)):
                self.x, self.y = self.targetX2, self.targetY2
                self.vX = self.v
                self.vY = 0
                if self.spawnSide == "left":
                    self.rotateImgs(90)
                else: self.rotateImgs(-90)
                self.animate()
    
    def checkTarget3(self):
        if (self.getDistance(self.x,self.y,self.targetX3,self.targetY3) 
            <= 10):
            self.x, self.y = self.targetX3, self.targetY3
            self.spawning = False
            self.movingToNormal = True 
            self.angle = 0
            self.frames = [self.baseImg1, self.baseImg2]
            self.vX = (self.normalX - self.x) // 40 
            self.vY = (self.normalY - self.y) // 40 
            self.mTNUpdates += 1
            self.animate()
        
    def checkDive(self): 
        if ((self.screenWidth > self.x > 0) and 
            not self.dive and self.y < self.screenHeight // 2 and
            random.randint(0, 1000) < 1): 
            self.dive = True 
            self.shoot = False 
            self.vX = random.choice([-5, 5])
            self.vY = 5
            self.frames = [self.baseImg1, self.baseImg2]
            self.boundLeft = max(30, self.x - random.randint(20, 40))
            self.boundRight = min(self.screenWidth - 30, 
                                    self.x + random.randint(20, 40))
            self.animate()
            
    def diveBounds(self):
        if self.x < self.boundLeft:
            self.vX = random.randint(2, 5)
            self.boundLeft = max(30, self.x - random.randint(5, 20))
        elif self.x > self.boundRight:
            self.vX = random.randint(-5, -2)
            self.boundRight = min(self.screenWidth - 30, 
                                self.x + random.randint(5, 20))
        # gets wider and wider, becoming more dangerous if left unchecked!
        
    def checkNormalMotion(self):
        if (self.movingToNormal and 
        self.getDistance(self.x,self.y,self.normalX,self.normalY) <= 
            2*(self.vY**2 + self.vX**2)**0.5):
            self.x = self.normalX
            self.y = self.normalY  
            self.vX, self.vY = 0, 0
        if self.normal: # external command by a function from the game 
            self.movingToNormal = False
            self.vX = 0.5 * (self.wave + 1)
            self.vY = 0.5 * (self.wave + 1)
    
    def updateMoveToNormalVelocity(self):
        if self.timer % 5 == 0:
            self.vX = (self.normalX - self.x) // (37 - 3 * self.mTNUpdates)
            self.vY = (self.normalY - self.y) // (37 - 3 * self.mTNUpdates)
            self.mTNUpdates += 1
            
    def normalBounds(self):
        if (self.x < (self.normalX - self.bound) or 
            self.x > (self.normalX + self.bound)):
            self.vX = -self.vX
            self.vY = -self.vY
            self.bounce = False
        if self.bounce == False and self.x == self.normalX:
            self.vY = -self.vY
        
######## Basic Helper Functions ########
    
    def rotateImgs(self, angle):
        self.img1 = pygame.transform.rotate(self.img1, angle)
        self.img2 = pygame.transform.rotate(self.img2, angle)
        self.frames = [self.img1, self.img2]
        self.animate()

    def getDistance(self, x1, y1, x2, y2):
        distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        return distance
    
    def triangulate(self, x1, y1, x2, y2): # using law of cosines :)
        opp = x2 - x1 
        adj = y2 -y1
        hyp = self.getDistance(x1, y1, x2, y2)
        angle = math.degrees(math.acos((adj**2 + hyp**2 - opp**2)/(2*adj*hyp)))
        return angle 
        
    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h, w, h)

    def animate(self): 
        self.frame = (self.frame + 1) % 2
        self.image = self.frames[self.frame]
        self.updateRect()
        
class Boss(Enemy): # boss enemy has 2 stages and can capture the ship 
    def __init__(self, x, y, wave, spawnOrder, spawnSide, flightPattern, 
                 screenWidth, screenHeight):
        super().__init__(x, y, wave, spawnOrder, spawnSide, flightPattern,
                         screenWidth, screenHeight)
        self.boss = True 
        self.lives = 2
        self.purple = False
        self.moveToCapture = False
        self.img1 = pygame.transform.scale(pygame.image.load(
                           "Images/BossGreen1.png"), (30, 30))
        self.baseImg1 = self.img1.copy()
        self.img2 = pygame.transform.scale(pygame.image.load(
                           "Images/BossGreen2.png"), (30, 30))
        self.baseImg2 = self.img2.copy()
        self.frames = [self.baseImg1, self.baseImg2] 
        self.captureFrame = -1
        self.captureBeamImgs = []
        self.captureBeamImgsVals = []
        for i in range(1, 11):
            x, y = 10 + 2*i, 10 + 5*i # up to 30, 60
            self.captureBeamImgsVals.append((x,y))
            self.captureBeamImgs.append(pygame.transform.scale(pygame.image.load(
                        "Images/capture%d.png" % i), (x, y)).convert_alpha())
        self.fullBeamImgs = []
        for i in range(1,3):
            x, y = 30, 60
            self.fullBeamImgs.append((pygame.transform.scale(pygame.image.load(
                    "Images/FullCapture%d.png" % i), (x, y))).convert_alpha())
        self.fullBeamFrame = 0
        self.capturing = False
        
    def update(self):
        # self.timer += 1 
        # if self.capturing:
        #     assert(self.y == self.screenHeight//2)
        #     self.captureMove()
        #     return # invincible during capture sequence except from bombs
        #     
        # elif self.moveToCapture:
        #     if (self.y - self.screenHeight//2 <= 5): 
        #         self.y = self.screenHeight//2
        #         self.timer = 0
        #         self.vY, self.vX = 0, 0
        #         self.capturing = True 
        #         self.moveToCapture = False
        #     else:
        #         self.vX, self.vY = 0, 3
        
        if self.lives == 1 and not self.purple:
            self.img1 = pygame.transform.scale(pygame.image.load(
                            "Images/BossPurple1.png"), (40, 40))
            self.baseImg1 = self.img1.copy()
            self.img2 = pygame.transform.scale(pygame.image.load(
                            "Images/BossPurple2.png"), (40, 40))
            self.baseImg2 = self.img2.copy()
            self.frames = [self.baseImg1, self.baseImg2]
            self.purple = True 
        if self.lives == 0: 
            self.kill()
            
        super().update()
            
    def rotateImgs(self, angle):
        pass # looks weird 
        
    def checkDive(self): 
        if (not self.moveToCapture and not self.capturing 
            and (self.screenWidth > self.x > 0) and 
            not self.dive and random.randint(0, 1000) < 1): 
            self.dive = True 
            self.shoot = False 
            self.vX = random.choice([-5, 5])
            self.vY = 7
            self.frames = [self.baseImg1, self.baseImg2]
            self.boundLeft = max(30, self.x - random.randint(20, 40))
            self.boundRight = min(self.screenWidth - 30, 
                                    self.x + random.randint(20, 40))
            self.animate()
            
    def captureMove(self):      
        if self.timer % 10 == 0:
            self.captureFrame += 1
            if self.captureFrame < len(self.captureBeamImgs): # first 
                beamW, beamH = self.captureBeamImgsVals[self.captureFrame]
                imageW = min(self.width + beamW//10, 40)
                imageH = min(self.height + beamH//5, 100)
                self.image = pygame.Surface((imageW, imageH))
                imgW, imgH = self.image.get_size()
                self.baseImg2.blit(self.image, (imgW//2, 0))
                self.captureBeamImgs[self.captureFrame].blit(self.image, (0,0))
            else: # next
                if self.captureFrame >= len(self.captureBeamImgsVals):
                    self.timer = 0 
                self.fullBeamFrame = (self.timer // 10) % 3 
                self.fullBeamImgs[self.fullBeamFrame].blit(self.image, (0,0))
                if self.timer >= 100: 
                    self.image = self.baseImg2
                    self.capturing = False
                    self.movingToNormal = True 
                    self.vX = (self.normalX - self.x) // 40 
                    self.vY = (self.normalY - self.y) // 40 
                    self.mTNUpdates += 1
                    self.animate()
        self.updateRect()
            
            