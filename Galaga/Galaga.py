## all uncited code is my own 
## Music from downloads.khinsider.com
## Images in Ship, Explosion, Powerup, and Bullets from spriters-resource.com
## References across all files: 
    # Pygame documentation
    # Lukas Peraza's 112 Pygame tutorial 
## Code Citations across all files:
    # updateRect and other very basic functions from Lukas Peraza's tutorial 

## please ignore code that is commented out due to debugging issues 

import random, string, math, os, pygame
from pygamegame import PygameGame
from Ship import Ship, Ship2
from Background import Background
from Bullets import Bullets, EnemyBullet
from Enemy import Enemy, Boss 
from Powerups import Powerups
from Explosion import Explosion, EnemyExplosion

pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

highscores = dict() # keys are user name input, values are their scores
highscores["112 "] = 9999
highscores["luvs"] = 99999
highscores["Habi"] = 999999
highscores["ba!!"] = 9999999

class Galaga(PygameGame): 
    def init(self):
        pygame.mixer.music.load("Music/Load.mp3")
        pygame.mixer.music.play()
        pygame.mixer.init()
        self.twoplayer = False 
        screenSize = (self.width, self.height)
        self.background = Background(screenSize)
        Ship.init()
        Ship2.init()
        self.ship1Group   = pygame.sprite.Group(Ship(self.width/2, self.height,
                                                    self.width, self.height))
        self.ship2Group   = pygame.sprite.Group()
        self.enemyGroup   = pygame.sprite.Group() 
        self.p1Bullets    = pygame.sprite.Group()
        self.p2Bullets    = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.powerups     = pygame.sprite.Group()
        self.exploGroup   = pygame.sprite.Group()
         
        self.p1Score, self.p2Score = 0, 0 
        self.level = 1
        self.p1Lives = 3
        self.p1Dead, self.p2Dead = False, False
        self.waves = 4 + self.level
        self.wavesMade = 0
        self.waveList = [0] * self.waves
        self.waveSize = self.width // 50
        self.timer = 0
        self.deathTimer = 0
        self.lastFire1, self.lastFire2 = 0, 0
        self.cleared = False 
        self.splashTime = 0 
        self.gameOver = False  
        self.menu = True 
        self.showHiScores = False
        self.name = ""
        self.lastSpawnDir = None
        self.ship1gun, self.ship2gun = "normal", "normal"
        self.currentPowerup = None 
        self.p1Captured, self.p2Captured = False, False 
        
    def almostEqual(self, a, b):
        dif = a - b
        epsilon = 10**-20
        return dif < epsilon
        
##############################################################################

    def redrawAll(self, screen):
        screen.fill( (0,0,0) )
        self.background.draw(screen) 
        self.exploGroup.draw(screen)
        self.powerups.draw(screen)
        self.p2Bullets.draw(screen)
        self.p1Bullets.draw(screen)
        self.enemyBullets.draw(screen)
        self.enemyGroup.draw(screen)
        self.ship1Group.draw(screen)
        if self.twoplayer:
            self.ship2Group.draw(screen)
        self.drawUI(screen)
        
    def drawUI(self, screen):
        if self.menu: 
            x1, y1 = 20, self.height // 8
            text = "GALAGA 112"
            self.drawText(screen, text, x1, y1, 36)
            x2, y2 = 30, self.height // 4
            text = "Press SPACE to play"
            self.drawText(screen, text, x2, y2, 18)
            if not self.twoplayer:            
                text = "Tab for 2 Player!"
                x3, y3 = self.width//7, self.height//3 
                self.drawText(screen, text, x3, y3, 17)
            text = "WASD or Arrow Keys to Move"
            x4, y4 = 40, self.height//2 
            self.drawText(screen, text, x4, y4, 12)
            text = "Tab or Space to Shoot"
            x5, y5 = 70, self.height//2 + 30 
            self.drawText(screen, text, x5, y5, 12)
            return 
            
        if self.twoplayer:
            self.twoplayerUI(screen)
        else: 
            self.onePlayerUI(screen)
        if self.cleared:
            text = "Level Cleared!"
            self.drawText(screen, text, 35, self.height/3)
            text = "Next Level: %d" % (self.level + 1)
            self.drawText(screen, text, 35, self.height/2)
        elif self.gameOver:
            text = "Game Over!"
            self.drawText(screen, text, 90, self.height//6)
            if self.p1Score >= self.p2Score:
                text = "P1,Insert Name: %s" % self.name
            else: 
                text = "P2,Insert Name: %s" % self.name
            self.drawText(screen, text, 20, self.height//3, 18)
            text = "Press SHIFT when done"
            self.drawText(screen, text, 10, self.height*3//4, 18)
        elif self.showHiScores:
            self.background.levelCleared = True  
            self.swapNames()
            self.drawText(screen, "LEADERBOARDS", 20, self.height//8, 30)
            text = "Click to restart"
            self.drawText(screen, text, 60, self.height*5//6, 18)
            for place, scoreName in enumerate(sorted(highscores.items())):
                score, name = scoreName
                text = "%d.%s:%d" % (5 - place, name, score)
                self.drawText(screen, text, 50, self.height//4 + place*50)
                if place == 4: break
    
    def initialize2P(self):
        self.ship2Group.add(Ship2(self.width//4, self.height, 
                                  self.width, self.height))
        self.p1Lives, self.p2Lives = 2, 2
        self.waves *= 2 
        self.waveList = [0] * self.waves
         
    def onePlayerUI(self, screen):
        score = "%d" % self.p1Score
        lives = "%d" % self.p1Lives 
        level = "Level %d" % self.level
        scoreX, scoreY = self.width/2 - 10, 0
        livesX, livesY = 0, self.height - 20
        levelX, levelY = self.width - 100, self.height - 20
        scoreSize, livesSize, levelSize = 12, 12, 12
        self.drawText(screen, score, scoreX, scoreY, scoreSize)
        self.drawText(screen, lives, livesX, livesY, livesSize)
        self.drawText(screen, level, levelX, levelY, levelSize)
        
    def twoplayerUI(self, screen):
        p1score = "P1:%d" % self.p1Score
        p2score = "P2:%d" % self.p2Score
        p1lives = "P1:%d" % self.p1Lives
        p2lives = "P2:%d" % self.p2Lives
        level = "Level %d" % self.level
        self.drawText(screen, p1score, 20, 0, 12)
        self.drawText(screen, p2score, self.width*2//3, 0, 12)
        self.drawText(screen, p1lives, 0, self.height - 20, 12)
        self.drawText(screen, p2lives, self.width*5//6, self.height - 20, 12)
        self.drawText(screen, level, self.width*2//5, self.height - 20, 12)
        
    def swapNames(self):
        global highscores
        newScores = dict()
        for name in highscores:
            if isinstance(name, str):
                score = highscores[name] 
                newScores[score] = name
            else: newScores[name] = highscores[name]
        highscores = newScores
        
    def drawText(self, screen, text, x, y, 
                 size = 24, color = (255,0,0), fontType = "GalagaText.ttf"):
        font = pygame.font.Font(fontType, size)
        text = font.render(text, False, color)
        screen.blit(text, (x, y))
            
##############################################################################
     
    def timerFired(self, dt):
        self.background.update(self.isKeyPressed) 
        if self.menu or not self.gameOver: 
            if not self.p1Dead or self.p1Captured:
                self.ship1Group.update(self.isKeyPressed, 
                                        self.width, self.height)
            if self.twoplayer:
                if not self.p2Dead or self.p2Captured:
                    self.ship2Group.update(self.isKeyPressed, 
                                            self.width, self.height)
        if self.menu: return 

####### timerFired during gameplay #######
        
        self.startEnemyMovement()
        self.enemyGroup.update()
        self.enemyShoot()
        self.exploGroup.update()                
        self.powerups.update()
        self.p1Bullets.update()
        self.p2Bullets.update()
        self.enemyBullets.update()
        # self.bossCaptureSequence()
        
        if self.gameOver or self.showHiScores: 
            return 
        
        if self.wavesMade == 0:  
            self.spawnWave() 
        if self.wavesMade < self.waves:  
            self.spawnPowerups()
            if self.timer == 0: 
                self.spawnWave()
            elif len(self.enemyGroup) == 0 or (self.timer % (self.fps*12) == 0):
                self.spawnWave() 
        else: 
            if (len(self.enemyGroup) == 0):
                self.cleared = True 
                self.background.levelCleared = True 
                self.nextLevel()

        self.checkWaveClear()
        
        if not self.twoplayer:
            self.checkDeath()
            self.check1PCollisions() 
        else:
            self.checkPlayerDeath()
            self.check2PCollisions()
        self.timer += 1 
        
    def nextLevel(self): # sets up for the next level 
        pygame.mixer.music.load("Music/NextLevel.mp3")
        pygame.mixer.music.play()
        self.splashTime += 1
        bonus = self.level * 1000
        incr = bonus //(self.fps * 5) 
        self.p1Score += incr
        self.p2Score += incr
        if self.splashTime > self.fps * 4:
            self.background.levelCleared = False
            self.background.starH = 5
        if self.splashTime > self.fps * 5:
            self.p1Score += bonus - self.splashTime * incr # for rounding error
            self.p2Score += bonus - self.splashTime * incr 
            self.level += 1
            if self.level % 5 == 0: 
                self.p1Lives = max(self.p1Lives + 1, 5)
            self.timer = 0
            self.lastFire1 = 0 
            self.cleared = False 
            self.splashTime = 0 
            self.waves = 4 + self.level 
            if self.twoplayer: 
                self.waves *= 2
            self.wavesMade = 0
            self.waveList = [0] * self.waves
        
    def spawnPowerups(self):
        if self.timer == 0 and self.level % 3 == 1:
            x = random.randint(20, self.width - 20)
            power = random.choice(["fan", "triple","bomb"])
            self.powerups.add(Powerups(x, power, self.height))
            self.currentPowerup = power 
            
    def bossCaptureSequence(self):
        for boss in self.enemyGroup:
            if boss.boss == True:
                if boss.lives < 2: 
                    continue 
                if boss.moveToCapture or boss.capturing:
                    break 
            
                if boss.normal and random.randint(0, 100) == 0:
                    boss.capturing = False
                    boss.moveToCapture = True
                    boss.timer = 0  
                    boss.vX = 0 
                    boss.vY = 3 
                    break
            
    def enemyShoot(self):
        for enemy in self.enemyGroup:
            if enemy.normal: continue 
            if enemy.shoot == False and random.randint(0, 300) < 1:
                y = enemy.y + enemy.height
                if enemy.dive: 
                    for x in ([enemy.x-10, enemy.x, enemy.x+10]):
                        self.enemyBullets.add(EnemyBullet(x, y))
                else:
                    x = enemy.x
                    self.enemyBullets.add(EnemyBullet(x, y))
                enemy.shoot = True 
                
    def startEnemyMovement(self): 
# enemies in normal wave position stay still until all living enemies are there
        for wave in self.waveList:
            if wave == 0:
                continue 
            move = True
            for enemy in self.enemyGroup:
                if move == False: 
                    break
                if enemy.dive: 
                    continue 
                if wave == enemy.normalY:
                    if (enemy.vX != 0 or enemy.vY != 0):
                        move = False
            if move:
                for enemy in self.enemyGroup:
                    if (wave == enemy.normalY and 
                        enemy.vX == 0 and enemy.vY == 0):
                        enemy.normal = True 
        
    def checkDeath(self):
        if self.p1Lives == 0:
            self.p1Dead = True 
            ship = self.ship1Group.sprites()[0]
            self.exploGroup.add(Explosion(ship.x, ship.y))
            self.ship1Group.empty()
            self.gameOver = True
            
    def checkPlayerDeath(self):
        if not self.p1Dead:
            ship1 = self.ship1Group.sprites()[0]
        if not self.p2Dead:
            ship2 = self.ship2Group.sprites()[0]
        if not self.p1Dead and self.p1Lives == 0:
            self.p1Dead = True 
            self.exploGroup.add(Explosion(ship1.x, ship1.y))
            self.ship1Group.empty()
        if not self.p2Dead and self.p2Lives == 0:
            self.p2Dead = True 
            self.exploGroup.add(Explosion(ship2.x, ship2.y))
            self.ship2Group.empty()
        if self.p1Dead and self.p2Dead:
            self.gameOver = True 
        
    def check1PCollisions(self):
        if self.gameOver: return 
        for enemy in pygame.sprite.groupcollide(self.enemyGroup, 
            self.p1Bullets, False, True):
            if not enemy.boss: 
                enemy.kill()
                self.p1Score += 100
                self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
            else: 
                enemy.lives -= 1
                if enemy.lives == 0: 
                    enemy.kill()
                    self.p1Score += 500
                    self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
            
        if len(self.ship1Group) == 1:
            if pygame.sprite.groupcollide(self.ship1Group, self.enemyGroup, 
                    False, True):
                    self.p1Lives -= 1
                    
        for enemyBullet in pygame.sprite.groupcollide(
            self.enemyBullets, self.ship1Group, True, False):
                self.p1Lives -= 1
        
        if pygame.sprite.groupcollide(self.powerups, self.ship1Group,  
            True, False):
            self.ship1gun = self.currentPowerup 
    
    def check2PCollisions(self):
        self.check1PCollisions()
        for enemy in pygame.sprite.groupcollide(self.enemyGroup, self.p2Bullets,
            False, True):
            if not enemy.boss: 
                enemy.kill()
                self.p1Score += 100
                self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
            else: 
                enemy.lives -= 1
                if enemy.lives == 0: 
                    enemy.kill()
                    self.p1Score += 500
                    self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
            
        if pygame.sprite.groupcollide(self.ship2Group, self.enemyGroup, 
            False, True):
            self.p2Lives -= 1 
            
        for enemyBullet in pygame.sprite.groupcollide(
            self.enemyBullets, self.ship2Group, True, False):
                self.p2Lives -= 1
                
        for powerup in pygame.sprite.groupcollide(
                self.ship2Group, self.powerups, False, True):
            self.ship2gun = self.currentPowerup
        
    def checkWaveClear(self):
        for i in range(len(self.waveList)):
            waveY = self.waveList[i] # the y value of all enemies in the wave
            if waveY == 0: 
                continue 
            waveCleared = True
            for enemy in self.enemyGroup:
                if enemy.normalY == waveY: 
                    waveCleared = False
            if waveCleared:
                self.waveList[i] = 0
    
    def findNextWave(self):
        for i in range(len(self.waveList)):
            if self.waveList[i] == 0:
                return i
        self.waveList.append(0)
        return len(self.waveList) - 1
        
    def spawnWave(self):
        wave  = self.findNextWave()
        self.waveList[wave] = 100 + 40 * wave
        y = self.waveList[wave]
        spawnSide = self.getSpawnSide()
        flightPattern = self.getFlightPattern("normal enemy")
        for spawnOrder in range(self.waveSize): 
            x = 45 * (1 + spawnOrder) - 5
            if wave == 0 and spawnOrder in range(2,6):
                self.enemyGroup.add(Boss(x, y, wave, spawnOrder, 
                spawnSide,flightPattern, self.width, self.height))
            else:
                self.enemyGroup.add(Enemy(x, y, wave, spawnOrder, 
                spawnSide,flightPattern, self.width, self.height))
        self.wavesMade += 1
        
    def getSpawnSide(self):
        if self.lastSpawnDir == None:
            self.lastSpawnDir = random.choice(["left","right"])
        else: 
            if self.lastSpawnDir == "left":
                self.lastSpawnDir = "right"
            else: 
                self.lastSpawnDir = "left"
        return self.lastSpawnDir
        
    def getFlightPattern(self, enemy): # called ***after*** getSpawnSide 
        spawnSide = self.lastSpawnDir
        x1 = random.randint(self.width//3, self.width//2)
        x3 = x1 + random.randint(100, 150)
        if spawnSide == "right":
            (x1, x3) = (x3, x1)
        x2 = x1 
        y1 = random.randint(self.height//6, self.height//3)
        y2 = y1 + random.randint(100, 150)
        y3 = y2
        flightPattern = [x1, y1, x2, y2, x3, y3]
        return flightPattern
        
##############################################################################

    def keyPressed(self, keyCode, modifier):
        if self.menu:
            if keyCode == pygame.K_TAB:
                self.twoplayer = True 
                self.initialize2P()
            if keyCode == pygame.K_SPACE:
                self.menu = False
        if not self.menu and not self.gameOver:
            if not self.p1Dead or self.p1Captured:
                if keyCode == pygame.K_SPACE:
                    if (self.timer - self.lastFire1) >= self.fps//4:
                        self.fire("p1")
            if self.twoplayer:
                if not self.p2Dead or self.p2Captured:
                    if keyCode == pygame.K_TAB:
                        if (self.timer - self.lastFire2) >= self.fps//2:
                             self.fire("p2")
                            
        if self.gameOver:
            if self.p1Score > self.p2Score: 
                score = self.p1Score
            else: score = self.p2Score
            if keyCode == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            if len(self.name) < 4:
                if chr(keyCode) in string.ascii_letters:
                    self.name += chr(keyCode)
            if keyCode == pygame.K_RSHIFT or keyCode == pygame.K_LSHIFT:
                self.swapNames()
                if self.name in highscores:
                    if score > highscore[self.name]:
                        highscores[self.p1Score] = self.name
                else:  
                    highscores[self.p1Score] = self.name
                
                self.gameOver = False
                self.showHiScores = True 
    
    def fire(self, player):
        if player == "p1":
            self.p1Fire()
        else: 
            self.p2Fire()
    
    def p1Fire(self):
        self.lastFire1 = self.timer 
        for i in range(len(self.ship1Group)):
            ship = self.ship1Group.sprites()[i]
            if self.ship1gun == "normal":
                self.p1Bullets.add(Bullets(ship.x, ship.y - 40, 0, self.height))
            elif self.ship1gun == "fan":
                for (i, x) in enumerate([ship.x - 10, ship.x, ship.x + 10]):
                    angle = (i - 1) * 10 
                    self.p1Bullets.add(Bullets(x, ship.y-10, angle, self.height))
            elif self.ship1gun == "triple":
                for x in [ship.x - 20, ship.x, ship.x + 20]:
                    self.p1Bullets.add(Bullets(x, ship.y - 10, 0, self.height))
            else:
                self.p1Score += 100*len(self.enemyGroup)//len(self.ship1Group)
                for enemy in self.enemyGroup:
                    self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
                    enemy.kill()
                self.ship1gun = "normal"
            
    def p2Fire(self):
        self.lastFire2 = self.timer 
        for i in range(len(self.ship2Group)):
            ship = self.ship2Group.sprites()[i]
            if self.ship2gun == "normal":
                self.p2Bullets.add(Bullets(ship.x, ship.y - 40, 0, self.height))
            elif self.ship2gun == "fan":
                for (i, x) in enumerate([ship.x - 10, ship.x, ship.x + 10]):
                    angle = (i - 2) * 10 
                    self.p2Bullets.add(Bullets(x, ship.y-10, angle, self.height))
            elif self.ship2gun == "triple":
                for x in [ship.x - 20, ship.x, ship.x + 20]:
                    self.p2Bullets.add(Bullets(x, ship.y - 10, 0, self.height))
            else:
                self.p2Score += 100*len(self.enemyGroup)//len(self.ship2Group)
                for enemy in self.enemyGroup:
                    self.exploGroup.add(EnemyExplosion(enemy.x, enemy.y))
                    enemy.kill()
                self.ship2gun = "normal"
            
    def mousePressed(self, x, y): 
        if self.showHiScores:
            self.init()
            
Galaga(400,500).run()
