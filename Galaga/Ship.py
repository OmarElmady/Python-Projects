# image from pixelartmaker.com
import pygame 
# a ship can move and be destroyed, 
# when destroyed it is not drawn and cannot be updated 
# cannot use attribute isDead, it has to be Galaga draw function and timerFired

class Ship(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Ship.shipImage = pygame.transform.scale(pygame.image.load(
        "images/ship.png"), (40, 50)).convert_alpha()
                        
    def __init__(self, x, y, screenWidth, screenHeight): 
        super().__init__()
        self.image = Ship.shipImage
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.x = x
        self.y = y
        self.dX, self.dY = 0, 0 
        self.updateRect()
        
    def update(self, keysDown, screenWidth, screenHeight):
        self.dX, self.dY = 0, 0
        if keysDown(pygame.K_LEFT):
            self.dX = -4
        elif keysDown(pygame.K_RIGHT):
            self.dX = 4 
        if keysDown(pygame.K_UP):
            self.dY = -5 
        elif keysDown(pygame.K_DOWN):
            self.dY = 5
        self.updateV()
        
    def updateV(self):
        self.x += self.dX 
        self.y += self.dY 
        self.x = min(max(self.x, self.width // 2 - 5), 
                        self.screenWidth - self.width // 2 - 5)
        self.y = min(max(self.y, self.screenHeight*5//6),
                         self.screenHeight - self.height//2)
        self.updateRect()

    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h, w, h)
        
class Ship2(Ship):
    @staticmethod
    def init():
        Ship.shipImage2 = pygame.transform.scale(pygame.image.load(
        "images/Ship2.png"), (37, 45)).convert_alpha()
        
    def __init__(self, x, y, screenWidth, screenHeight):
        super().__init__(x, y, screenWidth, screenHeight)
        self.image = Ship.shipImage2
        
    def update(self, keysDown, screenWidth, screenHeight):
        self.dX, self.dY = 0, 0 
        if keysDown(pygame.K_a):
            self.dX = -4
        elif keysDown(pygame.K_d):
            self.dX = 4 
        if keysDown(pygame.K_w):
            self.dY = -5 
        elif keysDown(pygame.K_s):
            self.dY = 5
        self.updateV()