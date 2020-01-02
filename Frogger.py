# Omar Elmady oelmady
from tkinter import *
import random  
    
class Frog(object):
    def __init__(self, data):
        self.col = data.cols // 2
        self.row = 0
        self.lives = 3
        self.collided = False
        
    def move(self, dir, data):
        if self.row >= data.rows - 1: # last row
            if self.col % 2 == 0: # if its an even col u win  
                data.win = True
            else: # landed in a bad square, too bad! 
                self.collided = True 
        self.checkCollision(data)
        if dir == "Up": 
            self.row = min(data.rows, self.row + 1)
        elif dir == "Down": 
            self.row = max(0, self.row - 1)
        elif dir == "Right": 
            self.col = min(data.cols -1, self.col + 1)
        elif dir == "Left": 
            self.col = max(0, self.col - 1)
        self.checkCollision(data)
        print ("frog = ", self.row, self.col)

    def checkCollision(self, data):
        for car in data.cars:
            self.collided = car.collidesWithFrog(self.row, self.col)
            if self.collided == True: break # 1 crash is enough for 1 frog 
        for truck in data.trucks:
            self.collided = truck.collidesWithFrog(self.row, self.col)
            if self.collided == True: break 
        if self.collided:
            self.lives -= 1
            self.col = data.cols // 2
            self.row = 0
            data.loss = True if (data.frog.lives == 0) else False
        self.collided = False 
        
    def draw(self, canvas, data):
        # bc row 0 is the bottom, add the height and decrease as row increases
        row, col = self.row, self.col  
        mX, mY = data.marginX, data.marginY  
        cS = data.cellSize  
        top    = (mX + cS * col + cS // 2,
                  data.height - cS * row)
        
        left   = (mX + cS * col, 
                  data.height - cS * (row + 1/2) )
        
        bottom = (mX + cS * col + cS // 2, 
                  data.height - cS * (row + 1) )
        
        right  = (mX + cS * (col + 1), 
                  data.height - cS * (row + 1/2) )
        canvas.create_polygon(top, left, bottom, right, fill = "brown")
        
class Vehicle(object):
    def __init__(self, row, col, data):
        self.row = row
        self.col = col        
        self.dir = data.dir[row] 
    
    def move(self):
        if self.dir == "left": 
            self.col -= 1 # move one spot left
        else: # right
            self.col += 1 
                
    def collidesWithFrog(self, frogX, frogY):
        if (self.row, self.col) == (frogX, frogY):
            return True 
        return False

    def __str__(self):
        return ("%d, %d" % (self.row, self.col))
        
class Car(Vehicle):
    def __init__(self, row, col, data):
        super().__init__(row, col, data)
        
    def draw(self, canvas, data):
        row, col = self.row, self.col
        mX, mY = data.marginX, data.marginY 
        cS = data.cellSize 
        
        topLeft  = (mX + cS * col, data.height - (mY + row * cS))
        botRight = (mX + cS * (col + 1), data.height - (mY + (row + 1) * cS))
        canvas.create_oval(topLeft, botRight, fill = "blue")
        
class Truck(Vehicle):
    def __init__(self, row, col, data):
        super().__init__(row, col, data)
        
    def collidesWithFrog(self, frogX, frogY):
        if (self.row, self.col) == (frogX, frogY):
            return True
        if self.dir == "left": # if its going left, col + 1 is also a collision 
            if (self.row, self.col + 1) == (frogX, frogY):
                return True
        else: # self.dir == "right"
            if (self.row, self.col - 1) == (frogX, frogY):
                return True
        return False
        
    def draw(self, canvas, data):
        row, col  = self.row, self.col 
        mX, mY = data.marginX, data.marginY 
        cS = data.cellSize 
        
        if self.dir == "left": # if its going left, the back half is to the right
            topLeft  = (mX + cS * col, data.height - (mY + (row + 1) * cS) )
            botRight = (mX + cS * (col + 2), data.height - (mY + row *cS) )
        else: # its going right
            topLeft  = (mX + cS * (col - 2), data.height - (mY + (row + 1)* cS))
            botRight = (mX + cS * col, data.height - (mY + row *cS) )
        canvas.create_rectangle(topLeft, botRight, fill = "red")
        
#############################################################################

def init(data):
    data.timerDelay = 1000 # seconds / 1000
    data.cellSize = 30 
    data.marginX = data.width % (data.cellSize//2) 
    data.marginY = data.height % (data.cellSize//2)
    data.rows, data.cols = data.height//data.cellSize, data.width//data.cellSize
    data.dir = makeDirList(data)
    data.cars = startVehicles(data, "Car") # (row,col) of starting cars
    data.trucks = startVehicles(data, "Truck") # ^ of starting trucks
    data.frog = Frog(data)
    # ^ 0 means left, 1 means right, each row has a set direction
    data.paused = False
    data.loss = False
    data.win = False

    
def timerFired(data):
    if (data.paused or data.loss or data.win): return # za warudo 
    moveVehicles(data)
    checkCrash(data) # check if we return frog.collided first 
    data.frog.checkCollision(data)
    if len(data.trucks + data.cars) <= (data.cols + 2*data.rows): 
        for i in range(random.randint(2, 2*2)):
            addVehicles(data)

def keyPressed(event, data):
    if event.keysym == "r": init(data) # restart! 
    elif event.keysym == "p": data.paused = not data.paused 
    elif event.keysym == "c":
        for car in data.cars:
            print ("car =", car.row, car.col)
    elif event.keysym == "t":
        for truck in data.trucks:
            print ("truck =", truck.row, truck.col)
     
    if (data.paused or data.loss or data.win): return # no inputs 
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        data.frog.move(event.keysym, data) 
    
def mousePressed(event, data): pass # no mice only frogs boi

def redrawAll(canvas, data):
    drawTerrain(canvas, data)
    data.frog.draw(canvas, data)
    for car in data.cars:
        car.draw(canvas, data)
    for truck in data.trucks:
        truck.draw(canvas, data)
    fontSize = 40
    if data.paused: 
        canvas.create_text(data.width/2, data.height/2, text = "PAUSED", 
                            fill = "green", font = "Helvetica %d" % fontSize)
    elif data.loss: 
        canvas.create_text(data.width/2, data.height/2, text = "YOU LOSE!", 
                            font = "Helvetica %d" % fontSize)
    elif data.win:       
        canvas.create_text(data.width/2, data.height/2, text = "YOU WIN!", 
                            font = "Helvetica %d" % fontSize)

#############################################################################

def makeDirList(data):
    dirList = []
    for dir in range(data.rows):
        if random.randint(0,1) == 0:
            dirList.append("left")
        else: dirList.append("right")
    return dirList

def startVehicles(data, type): # adds some random vehicles to start 
    numVehicles = random.randint(data.rows//2, data.rows) 
    vehicleList = [ ]
    for vehicle in range(numVehicles):
        row = random.randint(1, data.rows - 2)
        col = random.randint(0, data.cols) # random position
        if type == "Car":
            vehicleList.append( Car(row, col, data) ) 
        elif type == "Truck":
            vehicleList.append( Truck(row, col, data) )
    return vehicleList 
    
def checkCrash(data):
    print ("checking")
    for car in data.cars: 
        if car.collidesWithFrog(data.frog.row, data.frog.col):
            data.frog.collided = True  
    for truck in data.trucks:
        if truck.collidesWithFrog(data.frog.row, data.frog.col):
            data.frog.collided = True
    
def moveVehicles(data): # moves and also removes out of bounds vehicles 
    carList, truckList = [], []
    for car in data.cars: 
        car.move()
        if not ((car.col > data.rows) or (car.col < 0)): # car bounds
            carList.append(car)
    data.cars = carList # remove out of bounds cars 
    for truck in data.trucks:
        truck.move()
        if not ((truck.col > data.rows + 1) or (truck.col < -1)): #out of bounds
            truckList.append(truck)
    data.trucks = truckList
    
def addVehicles(data):
    row = random.randint(1, data.rows - 2) # first and last rows are special
    if data.dir[row] == "left":
        col = data.cols
    else: # dir == "right"
        col = 0 
    if ( ((row, col) in data.cars or data.trucks) or 
         ((row, col + 1) in data.cars or data.trucks) or 
         ((row, col - 1) in data.cars or data.trucks) ): 
        row = random.randint(1, data.rows - 2) 
    # prevents duplicates and provides some spacing 
    if random.randint(0,1) == 0: # a brand spanking new car, take that Ford!
       data.cars.append( Car(row, col, data) )
    else: # truck
        data.trucks.append(Truck(row, col, data))
 
def drawTerrain(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            color = "grey"
            if row == 0: color = "green"
            if row == data.rows - 1: 
                color = "black" if (col % 2 == 1) else "green"
            topLeft  = (data.marginX + col * data.cellSize, 
                        data.height - (data.marginY + row * data.cellSize))
            botRight = (data.marginX + (col + 1) * data.cellSize, 
                        data.height - (data.marginY + (row+1) * data.cellSize))
            canvas.create_rectangle(topLeft, botRight, fill = color)
            
#################################################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(300, 450)