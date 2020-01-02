import random, pygame, math
# background is made of stars 
class Background(object):
    stars = []
    
    def __init__(self, screenSize):  
        (self.screenW, self.screenH) = screenSize
        global stars 
        stars = self.stars = []
        for i in range(200):
            y = random.randint(0, self.screenH - 10)
            self.addStar(y) 
        self.levelCleared = False 
        self.starW = 3 
        self.starH = 5
        self.dX = 0
        self.dY = 3
        
    def addStar(self, y):
        x = random.randint(0, self.screenW - 4)
        colors = [ (204, 153, 0), (179, 36, 0), (0, 0, 153), (102, 0, 204), 
               (204, 255, 255), (230, 0, 230), (102, 255, 153) ] 
        color = random.choice(colors)
        self.stars.append( (x, y, color) )
    
    def update(self, keysDown):
        for i in range(len(self.stars)):
            (x, y, color) = self.stars[i]
            if keysDown(pygame.K_LEFT):
                if self.levelCleared: 
                    self.dX = 5 
                else: 
                    self.dX = 2
            elif keysDown(pygame.K_RIGHT):
                if self.levelCleared: 
                    self.dX = -5
                else:
                    self.dX = -2
            else: self.dX = 0
            
            if self.levelCleared: 
                if self.dY < 60:
                    self.dY += .005
                if self.starH < 60:
                    self.starH *= 1.0005
            else:
                if keysDown(pygame.K_UP):
                    self.dY = 8
                elif keysDown(pygame.K_DOWN):
                    self.dY = -2
                else: 
                    self.dY = 4

            x += self.dX
            y += self.dY
            if x < 0: 
                x = self.screenW
            elif x > self.screenW: 
                x = 0
            if y > self.screenH:  
                dif = y - self.screenH
                y = -dif - self.dY
            self.stars[i] = (x, y, color)
        
    def draw(self, screen):
        for star in self.stars:
            (x, y, color) = star
            pygame.draw.rect(screen, color, (x, y, self.starW, self.starH))
    