import pygame, random 

class Powerups(pygame.sprite.Sprite):
    def __init__(self, x, type, screenHeight):
        super().__init__() 
        if type == "fan":
            self.type = "fan"
            self.image = pygame.transform.scale(pygame.image.load(
                        "Images/fan.png"), (20,21))
        elif type == "triple":
            self.type = "triple"
            self.image = pygame.transform.scale(pygame.image.load(
                        "Images/triple.png"), (20,21))
        else: 
            self.type = "bomb"
            self.image = pygame.transform.scale(pygame.image.load(
                        "Images/bomb.png"), (20,21))
        self.x = x
        self.y = -10
        self.vY = 3 
        self.screenHeight = screenHeight
        self.updateRect()
        
    def update(self):
        if self.y > self.screenHeight: 
            self.kill()
        self.y += self.vY 
        self.updateRect()
        
    def updateRect(self): 
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h, w, h)
    