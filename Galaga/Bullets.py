import pygame, math, random

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, angle = 0, screenHeight = 500):
        super().__init__()
        self.x, self. y = x, y
        self.angle = angle 
        self.screenHeight = screenHeight
        self.image = pygame.transform.rotate(pygame.transform.scale( 
            pygame.image.load("Images/bullet.png"), 
                                (10,15)).convert_alpha(), -self.angle)
        self.v = 10 
        self.vX = self.v * math.sin(math.radians(self.angle))
        self.vY = -self.v * math.cos(math.radians(self.angle))
        self.updateRect()
    
    def updateRect(self): 
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h, w, h)
        
    def update(self):
        self.y += self.vY
        self.x += self.vX 
        if self.y < 0: self.kill()
        elif self.y > self.screenHeight: self.kill()
        self.updateRect()
        
class EnemyBullet(Bullets):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(pygame.image.load(
            "Images/enemybullet.png"), (10,15)).convert_alpha()
        self.vX, self.vY = random.randint(-3, 3), 5
        self.updateRect()