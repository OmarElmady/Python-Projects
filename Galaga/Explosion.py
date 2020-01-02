
import pygame, random
class Explosion(pygame.sprite.Sprite):
            
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 5):
            self.frames.append(pygame.transform.scale(pygame.image.load(
                "Images/playerExplosion%d.png" % i), 
                (60, 60)).convert_alpha())
        self.x, self.y = x, y
        self.frame = 0
        self.frameRate = 30
        self.aliveTime = random.randint(0, 2) # for spice

        self.updateImage()

    def updateImage(self): # from Lukas Peraza's demo 
        self.image = self.frames[self.frame]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self):
        if self.aliveTime % 6 == 5:
            self.frame += 1 
        if self.frame < len(self.frames):
            self.updateImage()
        else:
            self.kill()
            
        self.aliveTime += 1
            
class EnemyExplosion(Explosion):
    
    def __init__(self, x, y):
        super().__init__(x,y)
        self.frames = []
        for i in range(1, 5):
            self.frames.append(pygame.transform.scale(pygame.image.load(
                    "Images/enemyExplosion%d.png" % i), 
                    (8*(i+1), 8*(i+1))).convert_alpha())
        self.updateImage()