# Omar Elmady oelmady 
# Colaborators:  
# Matthew McQuaid mmcquaid 
# Mark Canavan mcanava1 
# Jacob Strieb jstrieb
# Ciro Baldinucci cbaldinu
################################################################################
# Helper Functions 
################################################################################
import random 
from tkinter import * 

def playTetris(rows = 15, cols = 10):
    margin = 25 
    cellSize = 35 # visibility  
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    run(width, height)
      
def getCellBounds(row, col, data):# from 112 site 
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    rowHeight = gridHeight / data.rows
    columnWidth = gridWidth / data.cols
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)
 
def makeBoard(rows, cols, data): #list comprehension 
    board=[]
    for row in range(rows): board += [ [data.emptyColor] * cols]
    return board
    
def drawBoard(canvas, rows, cols, data):
    canvas.create_rectangle(0,0, data.width, data.height, 
                            fill = "orange", width = 0)
    thiccness = 5 #magic numbers arent THICC
    for row in range(rows): #makes cells of the grid
        for col in range(cols):
            color = data.board[row][col]
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill = color, width = thiccness)
    
def drawGameOver(canvas, data): #to embarass losers 
    fontSize = data.width/12
    top, left = data.margin, data.margin + data.cellSize/2
    bottom = data.width - data.margin
    right = data.margin + data.cellSize * 2  
    canvas.create_rectangle(top, left, bottom, right, fill = "black")
    messageHeight = data.height/8 # to hide new block overlapping old one
    canvas.create_text(data.width/2, messageHeight, text = "Git Gud!",
                       fill = "yellow", 
                       font = "Helvetica %d" %fontSize) 
                    
def drawScore(canvas, data): #displays score
    scoreSize = 10
    width = data.width/2 - data.cellSize*.5 #to make it a bit more even
    canvas.create_text(width, 2, text = "Score: %d" % data.score, 
                       anchor = N, fill = "white", 
                       font = "Helvetica %d bold" % scoreSize)
    
def tetrisPieces(): #as per instructions
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    pieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]    
    return pieces
    
def newFallingPiece(data): #makes a random new falling block
    randIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randIndex]
    #new piece traits
    data.fallingPieceRow = 0 # top row 
    fallingPieceCols = len(data.fallingPiece[0]) 
    data.fallingPieceCol = data.cols//2 - fallingPieceCols//2 # ~center col
    
    if not isFallingPieceLegal(data): #if the newly spawned piece is illegal
        data.isGameOver = True 
    
def drawFallingPiece(canvas, data): #draws blocks of list-block 
    fallingPiece = data.fallingPiece 
    rows = len(fallingPiece)
    cols = len(fallingPiece[0])
    color = data.fallingPieceColor 
    thiccness = 5 #classy
    centerCol = data.fallingPieceCol * data.cellSize #proportional to board
    centerRow = data.fallingPieceRow * data.cellSize # ^
    for row in range(rows): 
        for col in range(cols):
            if fallingPiece[row][col] == True:
                (x0, y0, x1, y1) = getCellBounds(row, col, data) 
                x0 += centerCol #to center at start 
                x1 += centerCol
                y0 += centerRow 
                y1 += centerRow 
                canvas.create_rectangle(x0, y0, x1, y1, fill = color, 
                width = thiccness)

def moveFallingPiece(data, drow, dcol): #move according to input 
    oldRow = data.fallingPieceRow 
    oldCol = data.fallingPieceCol
    data.fallingPieceRow += drow #update position
    data.fallingPieceCol += dcol 
    if isFallingPieceLegal(data) == False: #move check undo
        data.fallingPieceRow = oldRow 
        data.fallingPieceCol = oldCol 
        return False #only relevant when drow = +1, but cleaner this way
    return True 
    
def isFallingPieceLegal(data): 
    row = data.fallingPieceRow
    col = data.fallingPieceCol 
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True: #if its a block
                if ((row + i >= 0) and (row + i < data.rows) and 
                    (col + j >= 0) and (col + j < data.cols)) == False: 
                    return False # if out of bounds
                if data.board[row+i][col+j] != data.emptyColor:            
                    return False # or on top of a block 
    return True
    
def rotateFallingPiece(data):
    oldPiece = data.fallingPiece #save old data
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    newNumRows, newNumCols = oldNumCols, oldNumRows #switcheroo 
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    newCol = oldCol + oldNumCols//2 - newNumCols//2
    newPiece = [([None] * newNumCols) for row in range(newNumRows)]
    for row in range(oldNumRows): #recreate block in a rotated position
        for col in range(oldNumCols):
            newPiece[(oldNumCols - 1) - col][row] = oldPiece[row][col]
    data.fallingPiece = newPiece #update block 
    data.fallingPieceRow, data.fallingPieceCol = newRow, newCol 
    if not isFallingPieceLegal(data): #restore old pos in case of failure
        data.fallingPiece = oldPiece 
        data.fallingPieceRow, data.fallingPieceCol = oldRow, oldCol
        
def placeFallingBlock(data):
    row = data.fallingPieceRow
    col = data.fallingPieceCol 
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):  
            if data.fallingPiece[i][j] == True: #if its a block
                data.board[row+i][col+j] = data.fallingPieceColor #place it 
    data.score += removeFullRows(data)**2 #add points 
    newFallingPiece(data) #makes a new piece

def removeFullRows(data):
    newBoard = [] 
    fullRows = 0 
    for row in range(data.rows):
        isFullRow = True 
        for col in range(data.cols):
            if (data.board[row][col] == data.emptyColor): 
                isFullRow = False #if any block is empty its not full 
        if isFullRow == False: newBoard.append(data.board[row]) #add it
        else: fullRows += 1 #dont add it if its full 
        
    if fullRows > 0: #only remake the board if we have to
        for row in range(fullRows): #ad
            newBoard.insert(0, [data.emptyColor] * data.cols)
        data.board = newBoard # if there was a full row we replace the board
    return fullRows 
    
##############################################################################
#MVC 
###############################################################################

def init(data):
    data.timerDelay = 500
    data.rows, data.cols = 15, 10 
    data.cellSize, data.margin = 35, 25 
    data.emptyColor = "blue"
    data.board = makeBoard(data.rows, data.cols, data)
    data.tetrisPieces = tetrisPieces()
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                                "cyan", "green", "orange" ]
    randIndex = random.randint(0, len(data.tetrisPieces) - 1)#random start block
    data.fallingPiece = data.tetrisPieces[randIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randIndex]                          
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2 
    data.isGameOver = False
    data.score = 0 
    
def keyPressed(event, data):
    if event.keysym == "r": init(data)
    if not data.isGameOver:
        if event.keysym == "Left": moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right": moveFallingPiece(data, 0, +1)
        elif event.keysym == "Down": moveFallingPiece(data, +1, 0)
        elif event.keysym == "Up": rotateFallingPiece(data)
         
def step(data):
    if moveFallingPiece(data, +1, 0) == False:
        placeFallingBlock(data)
        
def timerFired(data):
    if not data.isGameOver: 
        step(data)
    
def redrawAll(canvas, data):
    drawBoard(canvas, data.rows, data.cols, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if data.isGameOver: drawGameOver(canvas, data)
    
################################################################################
# Run Module 
################################################################################
    
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
    data.timerDelay = 10 # milliseconds
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
    # and launch the
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()