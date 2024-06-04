from abc import ABC, abstractmethod
from copy import copy, deepcopy
import pawnstarsHelpers as pH

def calculateAttackedBy(board): #function used to tell each piece what it is being attacked by
        
    #for every piece on the board
    for y in range(0,8): 
        for x in range(0,8):
            if(board[y][x].colour != -1):
                currPiece = board[y][x]
                currPiece.attackedBy = []
                #check every piece of the opposite colour to see if it attacks currPiece    
                for y2 in range(0, 8):
                    for x2 in range(0, 8):
                        if(board[y2][x2].colour != -1 and board[y2][x2].colour != currPiece.colour):
                            for i in board[y2][x2].isAttacking: # i is a piece being attacked by board[y][x]
                                if(i == currPiece): 
                                    currPiece.attackedBy.append(board[y2][x2])

class Piece(ABC):
    def __init__(self, name, colour, value, startPosX, startPosY):
        self.name = name
        self.colour = colour
        self.value = value
        self.startPos = [startPosY, startPosX]
        self.positionX = startPosX
        self.positionY = startPosY
        self.legalMoves = []
        self.isAttacking = []
        self.attackedBy = []

    @abstractmethod
    def getLegalMoves(self, board, conf, AIMove):
        pass

    def makeMove(self, board, moveNum, deadPieces, lookAhead): # function used to make a move, and check if move is a special move
        
        if((self.name == "wK" or self.name == "bK") and self.hasMoved == False): #if the piece is a king that hasnt moved
            selectedMove = self.legalMoves[moveNum] # gets the selected move of the selected piece
            if(isinstance(board[selectedMove[0]][selectedMove[1]], Rook)): # checks if the king wants to move to the rook
                if(selectedMove[1] < self.positionX): #rook is on left of king
                    leftRook = board[selectedMove[0]][selectedMove[1]]
                    board[selectedMove[0]][selectedMove[1]] = Empty()
                    board[self.positionY][self.positionX] = Empty()
                    
                    #update rooks position
                    board[self.positionY][self.positionX- 1] = leftRook
                    leftRook.positionY = self.positionY
                    leftRook.positionX = self.positionX - 1
                    leftRook.hasMoved = True
                    
                    #update position of king
                    board[self.positionY][self.positionX - 2] = self
                    self.positionY = self.positionY
                    self.positionX = self.positionX - 2
                    self.hasMoved = True
                else: # rook is on right of king
                    rightRook = board[selectedMove[0]][selectedMove[1]]
                    board[selectedMove[0]][selectedMove[1]] = Empty()
                    board[self.positionY][self.positionX] = Empty()
                    
                    #update rooks position
                    board[self.positionY][self.positionX + 1] = rightRook
                    rightRook.positionY = self.positionY
                    rightRook.positionX = self.positionX + 1
                    rightRook.hasMoved = True
                    
                    #update position of king
                    board[self.positionY][self.positionX + 2] = self
                    self.positionY = self.positionY
                    self.positionX = self.positionX + 2
                    self.hasMoved = True
            else: #not a castle
                
                board[self.positionY][self.positionX] = Empty() #sets the current position of the selected piece to be empty
                
                #if piece being moved is moving onto another piece, add dead piece to array of dead pieces
                if(board[selectedMove[0]][selectedMove[1]].colour != -1 and board[selectedMove[0]][selectedMove[1]].colour != self.colour): 
                    deadPieces.append(board[selectedMove[0]][selectedMove[1]])
                
                #set new position of piece 
                self.positionY = selectedMove[0]
                self.positionX = selectedMove[1]
                #update board
                board[selectedMove[0]][selectedMove[1]] = self
                self.hasMoved = True
        else: # non-king piece or king has already moved
            selectedMove = self.legalMoves[moveNum] #gets the selected move of the selected piece
            board[self.positionY][self.positionX] = Empty() #sets the current position of the selected piece to be empty
            
            #if piece being moved is moving onto another piece, add dead piece to array of dead pieces
            if(board[selectedMove[0]][selectedMove[1]].colour != -1 and board[selectedMove[0]][selectedMove[1]].colour != self.colour): 
                deadPieces.append(board[selectedMove[0]][selectedMove[1]])
            
            #set new position of piece 
            self.positionY = selectedMove[0]
            self.positionX = selectedMove[1]
            
            # pawn promotion checking
            
            if (isinstance(self, Pawn) and (self.positionY == 7 or self.positionY == 0) and lookAhead == False): 
                if(self.colour == 0 and self.positionY == 7): #white
                    newPiece = self.promotion(False)
                    board[self.positionY][self.positionX] = newPiece
                    deadPieces.append(self)
                elif(self.colour == 1 and self.positionY == 0): #black
                    newPiece = self.promotion(False)
                    board[self.positionY][self.positionX] = newPiece
                    deadPieces.append(self)
            else: #NORMAL MOVEMENT OF ANY NON PROMOTING PIECE
                #update board
                board[selectedMove[0]][selectedMove[1]] = self
            
            #if the piece being moved is a king or rook
            if((self.name == "wR" or self.name == "bR") and self.hasMoved == False):
                self.hasMoved == True
                      
    def confirmLegalMove(self, board, move): # confirms whether a move is legal by checking a hypothetical next board and seeing if rules are violated
        nextBoard = []
        nextDeads = []
        
        #copies board as to not affect it
        for row in range(0, 8):
            nextBoard.append([])
            for i in range(0, 8):
                nextBoard[row].append(deepcopy(board[row][i])) 
        
        currPiece = nextBoard[self.positionY][self.positionX] #
        
        moveNum = currPiece.legalMoves.index(move)
        currPiece.makeMove(nextBoard, moveNum, nextDeads, True) #make the move that is being examined on nextboard
        
        #calculate all legal moves on nextboard
        for y in range(0, 8):
            for x in range(0, 8):
                if(nextBoard[y][x].name != "."):
                    nextBoard[y][x].getLegalMoves(nextBoard, False, True)
    
        #calculate what each piece is being attacked by
        calculateAttackedBy(nextBoard)
        
        #get the kings on board
        Wk, Bk = pH.getKings(nextBoard)
                    
        if(Wk == None or Bk == None): #if the move made on nextboard kills the opposing players king (keep move to look at castling, should never get a chance to play it)
            return True
 
        #check if the king of the same colour as the selected piece is in check as a result of that move
        isChecked = False
        if(currPiece.colour == Wk.colour): #white piece
            isChecked = Wk.checkCheck()
        elif(currPiece.colour == Bk.colour): #black piece
            isChecked = Bk.checkCheck()
            
        return isChecked        
    
class Empty(Piece):
    def __init__(self):
        super().__init__(".", -1,  0, 0, 0)
        
    def getLegalMoves(self, board, conf, AIMove):
        pass
    
class Pawn(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  1, startPosX, startPosY)

    def getLegalMoves(self, board, conf, AIMove): #PAWNS MOVES
        self.legalMoves = []
        self.isAttacking = []
        self.attackedBy
        if(self.colour == 0): # white
            
            if((self.positionY == self.startPos[0]) and (self.positionX == self.startPos[1]) and (board[self.positionY + 1][self.positionX].colour == -1) and (board[self.positionY + 2][self.positionX].colour == -1)): # if this is the pawns first move
                
                self.legalMoves.append([self.positionY + 2, self.positionX])

            if((self.positionY + 1 <= 7) and (board[self.positionY + 1][self.positionX].colour == -1)): # if space infront is empty
                self.legalMoves.append([self.positionY + 1 , self.positionX])

            if((self.positionY + 1 <= 7) and (self.positionX + 1 <= 7) and (board[self.positionY + 1][self.positionX + 1].colour == 1)): # attack right
                self.legalMoves.append([self.positionY + 1 , self.positionX + 1])
                self.isAttacking.append(board[self.positionY + 1][self.positionX + 1])

            if((self.positionY + 1 <= 7) and (self.positionX - 1 >= 0) and (board[self.positionY + 1][self.positionX -1].colour == 1)): # attack left
                self.legalMoves.append([self.positionY + 1 , self.positionX - 1])
                self.isAttacking.append(board[self.positionY + 1][self.positionX -1])

                
        elif(self.colour == 1): # black
            
            if((self.positionY == self.startPos[0]) and (self.positionX == self.startPos[1]) and (board[self.positionY - 1][self.positionX].colour == -1) and (board[self.positionY - 2][self.positionX].colour == -1)): # if this is the pawns first move
                self.legalMoves.append([self.positionY - 2, self.positionX])
            
            if((self.positionY - 1 >= 0) and (board[self.positionY - 1][self.positionX].colour == -1)): # if space infront is empty
                self.legalMoves.append([self.positionY - 1 , self.positionX])
                
            if((self.positionY - 1 >= 0) and (self.positionX + 1 <= 7) and (board[self.positionY - 1][self.positionX + 1].colour == 0)): # attack right
                self.legalMoves.append([self.positionY - 1 , self.positionX + 1])
                self.isAttacking.append(board[self.positionY - 1][self.positionX + 1])
    
            if((self.positionY - 1 >= 0) and (self.positionX - 1 >= 0) and (board[self.positionY - 1][self.positionX -1].colour == 0)): # attack left
                self.legalMoves.append([self.positionY - 1 , self.positionX - 1])
                self.isAttacking.append(board[self.positionY - 1][self.positionX -1])
        
        if(conf == True and AIMove == False): 
            newLegals = copy(self.legalMoves)
            for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                if(isChecked == True):
                    newLegals.remove(i)
            self.legalMoves = copy(newLegals)
            
    def promotion(self, isAI): #PROMOTION OF PAWNS
        valid = False
        if(isAI == True):
            if(self.colour == 0): #white
                return Queen("wQ", 0, self.positionX, self.positionY)
            else:
                return Queen("bQ", 1, self.positionX, self.positionY)
        else:
            while(valid == False):
                userInput = input("Promote pawn at " + str(self.positionY + 1) +  " " + str(self.positionX + 1) + " to: (Queen, Rook, Bishop, Knight) ")
                if(userInput == "Queen"):
                    if(self.colour == 0): #white
                        return Queen("wQ", 0, self.positionX, self.positionY)
                    else:
                        return Queen("bQ", 1, self.positionX, self.positionY)
                elif(userInput == "Rook"):
                    if(self.colour == 0): #white
                        return Rook("wR", 0, self.positionX, self.positionY)
                    else:
                        return Rook("bR", 1, self.positionX, self.positionY)
                elif(userInput == "Bishop"):
                    if(self.colour == 0): #white
                        return Bishop("wB", 0, self.positionX, self.positionY)
                    else:
                        return Bishop("bB", 1, self.positionX, self.positionY)
                elif(userInput == "Knight"):
                    if(self.colour == 0): #white
                        return Knight("wN", 0, self.positionX, self.positionY)
                    else:
                        return Knight("bN", 1, self.positionX, self.positionY)
                else:
                    print("Invalid input!")
        
            
                  
class Knight(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  3, startPosX, startPosY)
        
    def getLegalMoves(self, board, conf, AIMove): #KNIGHTS MOVES
        self.legalMoves = []
        self.isAttacking = []

        if((self.positionY + 2 <= 7 ) and (self.positionX + 1 <= 7) and (self.colour != board[self.positionY + 2][self.positionX + 1].colour)): # up and right
            movePos = board[self.positionY + 2][self.positionX + 1]
            self.legalMoves.append([self.positionY + 2, self.positionX + 1])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
        
        if((self.positionY + 2 <= 7 ) and (self.positionX - 1 >= 0) and (self.colour != board[self.positionY + 2][self.positionX - 1].colour)): #up and left
            movePos = board[self.positionY + 2][self.positionX - 1]
            self.legalMoves.append([self.positionY + 2, self.positionX - 1])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
        
        if((self.positionY - 2 >= 0) and (self.positionX + 1 <= 7) and (self.colour != board[self.positionY - 2][self.positionX + 1].colour)): #down and right
            movePos = board[self.positionY - 2][self.positionX + 1]
            self.legalMoves.append([self.positionY - 2, self.positionX + 1])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
       
        if((self.positionY - 2 >= 0) and (self.positionX - 1 >= 0) and (self.colour != board[self.positionY - 2][self.positionX - 1].colour)): #down and left
            movePos = board[self.positionY - 2][self.positionX - 1]
            self.legalMoves.append([self.positionY - 2, self.positionX - 1])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
        
        if((self.positionY + 1 <= 7) and (self.positionX - 2 >= 0) and (self.colour != board[self.positionY + 1][self.positionX - 2].colour)): #left and up
            movePos = board[self.positionY + 1][self.positionX - 2]
            self.legalMoves.append([self.positionY + 1, self.positionX - 2])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
        
        if((self.positionY - 1 >= 0) and (self.positionX - 2 >= 0) and (self.colour != board[self.positionY - 1][self.positionX - 2].colour)): #left and down
            movePos = board[self.positionY - 1][self.positionX - 2]
            self.legalMoves.append([self.positionY - 1, self.positionX - 2])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
         
        if((self.positionY + 1 <= 7) and (self.positionX + 2 <= 7) and (self.colour != board[self.positionY + 1][self.positionX + 2].colour)): #right and up
            movePos = board[self.positionY + 1][self.positionX + 2]
            self.legalMoves.append([self.positionY + 1, self.positionX + 2])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
        
        
        if((self.positionY - 1 >= 0) and (self.positionX + 2 <= 7) and (self.colour != board[self.positionY - 1][self.positionX + 2].colour)): #right and down
            movePos = board[self.positionY - 1][self.positionX + 2]
            self.legalMoves.append([self.positionY - 1, self.positionX + 2])
            if(self.colour != movePos.colour and movePos.colour != -1):
                self.isAttacking.append(movePos)
                
        if(conf == True and AIMove == False): 
            newLegals = copy(self.legalMoves)
            for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                if(isChecked == True):
                    newLegals.remove(i)
            self.legalMoves = copy(newLegals)

            
class Bishop(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  3, startPosX, startPosY)
            
    def getLegalMoves(self, board, conf, AIMove): #BISHOPS MOVES
        self.legalMoves = []
        self.isAttacking = []
        if ((self.positionY > 0) and self.positionX > 0): #left up
            x = self.positionX - 1
            for y in range(self.positionY - 1, -1, -1):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y - 1 < 0 or x - 1 < 0):
                    break
                
                x -= 1
                
        if((self.positionY > 0) and (self.positionX < 7)): #right up
            x = self.positionX + 1
            for y in range(self.positionY - 1, -1, -1):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
            
                if(y - 1 < 0 or x + 1 > 7):
                    break
        
                x += 1
                
        if((self.positionY < 7) and (self.positionX < 7)): #right down
            x = self.positionX + 1
            for y in range(self.positionY + 1, 8):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7 or x + 1 > 7):
                    break
                
                x += 1
                
        if((self.positionY < 7) and (self.positionX > 0)): #left down
            x = self.positionX - 1
            for y in range(self.positionY + 1, 8):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7 or x + 1 > 7):
                    break
                
                x -= 1
    
        if(conf == True and AIMove == False): 
                newLegals = copy(self.legalMoves)
                for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                    isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                    if(isChecked == True):
                        newLegals.remove(i)
                self.legalMoves = copy(newLegals)   
                
class Rook(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  5, startPosX, startPosY)
        self.hasMoved = False
        
    def getLegalMoves(self, board, conf, AIMove): #ROOKS MOVES
        self.legalMoves = []
        self.isAttacking = []
        if(self.positionY < 7): # move down
            for y in range(self.positionY + 1, 8):
                if(board[y][self.positionX].colour == -1):                     #empty space
                    self.legalMoves.append([y, self.positionX])
                elif(board[y][self.positionX].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, self.positionX])
                    self.isAttacking.append(board[y][self.positionX])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7):
                    break
                
        if(self.positionY > 0): # move up
                for y in range(self.positionY - 1, -1, -1):
                    if(board[y][self.positionX].colour == -1):                     #empty space
                        self.legalMoves.append([y, self.positionX])
                    elif(board[y][self.positionX].colour != self.colour): #found piece of opposite colour (first blockage)
                        self.legalMoves.append([y, self.positionX])
                        self.isAttacking.append(board[y][self.positionX])
                        
                        break
                    else:                                                       #found piece to be same colour (first blockage)
                        break
                    
                    if(y - 1 < 0):
                        break
        
        if(self.positionX < 7): # move right
            for x in range(self.positionX + 1, 8):
                if(board[self.positionY][x].colour == -1):                         #empty space
                    self.legalMoves.append([self.positionY, x])
                elif(board[self.positionY][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([self.positionY, x])
                    self.isAttacking.append(board[self.positionY][x])
                    
                    break
                else:                                                       #found piece to be same colour (first blockage)
                    break
                
                if(x + 1 > 7):
                    break
                
        if(self.positionX > 0): #move left
            for x in range(self.positionX - 1, -1, -1):
                if(board[self.positionY][x].colour == -1):                         #empty space
                    self.legalMoves.append([self.positionY, x])
                elif(board[self.positionY][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([self.positionY, x])
                    self.isAttacking.append(board[self.positionY][x])
                    
                    break
                else:                                                       #found piece to be same colour (first blockage)
                    break
                
                if(x - 1 < 0):
                    break
                
        if(conf == True and AIMove == False): 
            newLegals = copy(self.legalMoves)
            for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                if(isChecked == True):
                    newLegals.remove(i)
            self.legalMoves = copy(newLegals)

                  
class Queen(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  50, startPosX, startPosY)
        
    def getLegalMoves(self, board, conf, AIMove): #QUEENS MOVES
        self.legalMoves = []
        self.isAttacking = []
        if ((self.positionY > 0) and self.positionX > 0): #left up
            x = self.positionX - 1
            for y in range(self.positionY - 1, -1, -1):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y - 1 < 0 or x - 1 < 0):
                    break
                
                x -= 1
                
        if((self.positionY > 0) and (self.positionX < 7)): #right up
            x = self.positionX + 1
            for y in range(self.positionY - 1, -1, -1):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
            
                if(y - 1 < 0 or x + 1 > 7):
                    break
        
                x += 1
                
        if((self.positionY < 7) and (self.positionX < 7)): #right down
            x = self.positionX + 1
            for y in range(self.positionY + 1, 8):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7 or x + 1 > 7):
                    break
                
                x += 1
                
        if((self.positionY < 7) and (self.positionX > 0)): #left down
            x = self.positionX - 1
            for y in range(self.positionY + 1, 8):
                if(board[y][x].colour == -1):                     #empty space
                    self.legalMoves.append([y, x])
                elif(board[y][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, x])
                    self.isAttacking.append(board[y][x])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7 or x + 1 > 7):
                    break
                
                x -= 1
                
        if(self.positionY < 7): # move down
            for y in range(self.positionY + 1, 8):
                if(board[y][self.positionX].colour == -1):                     #empty space
                    self.legalMoves.append([y, self.positionX])
                elif(board[y][self.positionX].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([y, self.positionX])
                    self.isAttacking.append(board[y][self.positionX])
                    
                    break
                else:                                       #found piece to be same colour (first blockage)
                    break
                
                if(y + 1 > 7):
                    break
                
        if(self.positionY > 0): # move up
                for y in range(self.positionY - 1, -1, -1):
                    if(board[y][self.positionX].colour == -1):                     #empty space
                        self.legalMoves.append([y, self.positionX])
                    elif(board[y][self.positionX].colour != self.colour): #found piece of opposite colour (first blockage)
                        self.legalMoves.append([y, self.positionX])
                        self.isAttacking.append(board[y][self.positionX])
                        
                        break
                    else:                                                       #found piece to be same colour (first blockage)
                        break
                    
                    if(y - 1 < 0):
                        break
        
        if(self.positionX < 7): # move right
            for x in range(self.positionX + 1, 8):
                if(board[self.positionY][x].colour == -1):                         #empty space
                    self.legalMoves.append([self.positionY, x])
                elif(board[self.positionY][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([self.positionY, x])
                    self.isAttacking.append(board[self.positionY][x])
                    
                    break
                else:                                                       #found piece to be same colour (first blockage)
                    break
                
                if(x + 1 > 7):
                    break
                
        if(self.positionX > 0): #move left
            for x in range(self.positionX - 1, -1, -1):
                if(board[self.positionY][x].colour == -1):                         #empty space
                    self.legalMoves.append([self.positionY, x])
                elif(board[self.positionY][x].colour != self.colour): #found piece of opposite colour (first blockage)
                    self.legalMoves.append([self.positionY, x])
                    self.isAttacking.append(board[self.positionY][x])
                    
                    break
                else:                                                       #found piece to be same colour (first blockage)
                    break
                
                if(x - 1 < 0):
                    break
                
        if(conf == True and AIMove == False): 
            newLegals = copy(self.legalMoves)
            for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                if(isChecked == True):
                    newLegals.remove(i)
            self.legalMoves = copy(newLegals)

        
class King(Piece):
    def __init__(self, name, colour, startPosX, startPosY):
        super().__init__(name, colour,  100, startPosX, startPosY)
        self.isChecked = False
        self.hasMoved = False
        
    def getLegalMoves(self, board, conf, AIMove): # KINGS MOVES
        self.legalMoves = []
        self.isAttacking = []
        
        if((self.positionY + 1 <= 7) and (board[self.positionY + 1][self.positionX].colour == -1 or board[self.positionY + 1][self.positionX].colour != self.colour)): # up
            self.legalMoves.append([self.positionY + 1, self.positionX])
            if(board[self.positionY + 1][self.positionX].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY + 1][self.positionX])
            
        if((self.positionY + 1 <= 7) and (self.positionX + 1 <= 7) and (board[self.positionY + 1][self.positionX + 1].colour == -1 or board[self.positionY + 1][self.positionX + 1].colour != self.colour)): # down right
            self.legalMoves.append([self.positionY + 1, self.positionX + 1])
            if(board[self.positionY + 1][self.positionX + 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY + 1][self.positionX + 1])
        
        if((self.positionX + 1 <= 7) and (board[self.positionY][self.positionX + 1].colour == -1 or board[self.positionY][self.positionX + 1].colour != self.colour)): # right
            self.legalMoves.append([self.positionY, self.positionX + 1])
            if(board[self.positionY][self.positionX + 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY][self.positionX + 1])
            
        if((self.positionY - 1 >= 0) and (self.positionX + 1 <= 7) and (board[self.positionY - 1][self.positionX + 1].colour == -1 or board[self.positionY - 1][self.positionX + 1].colour != self.colour)): # up right
            self.legalMoves.append([self.positionY - 1, self.positionX + 1])
            if(board[self.positionY - 1][self.positionX + 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY - 1][self.positionX + 1])
            
        if((self.positionY - 1 >= 0) and (board[self.positionY - 1][self.positionX].colour == -1 or board[self.positionY - 1][self.positionX].colour != self.colour)): # down
            self.legalMoves.append([self.positionY - 1, self.positionX])
            if(board[self.positionY - 1][self.positionX].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY - 1][self.positionX])
            
        if((self.positionY - 1 >= 0) and (self.positionX - 1 >= 0) and (board[self.positionY - 1][self.positionX - 1].colour == -1 or board[self.positionY - 1][self.positionX - 1].colour != self.colour)): # up left
            self.legalMoves.append([self.positionY - 1, self.positionX - 1])
            if(board[self.positionY - 1][self.positionX - 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY - 1][self.positionX - 1])
            
        if((self.positionX - 1 >= 0) and (board[self.positionY][self.positionX - 1].colour == -1 or board[self.positionY][self.positionX - 1].colour != self.colour)): # left
            self.legalMoves.append([self.positionY, self.positionX - 1])
            if(board[self.positionY][self.positionX - 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY][self.positionX - 1])
            
        if((self.positionY + 1 <= 7) and (self.positionX - 1 >= 0) and (board[self.positionY + 1][self.positionX - 1].colour == -1 or board[self.positionY + 1][self.positionX - 1].colour != self.colour)): # down left
            self.legalMoves.append([self.positionY + 1, self.positionX - 1])
            if(board[self.positionY + 1][self.positionX - 1].colour != -1): # is enemy piece
                self.isAttacking.append(board[self.positionY + 1][self.positionX - 1])
            
        #CASTLING SETUP
        if(self.hasMoved == False and self.colour == 0): #white king
            #left rook
            if((board[0][0].name == "wR" and board[0][0].hasMoved == False) and board[0][1].name == "." and board[0][2].name == "."):
                valid = True
                positions = [[0,0], [0,1], [0,2], [0,3]]
                for y in range(0,8):
                    for x in range(0,8):
                        if(board[y][x].colour == 1): #if the piece is black
                            for attack in board[y][x].legalMoves:
                                if(attack in positions): #if a piece of the opposite colour is attacking either the king, rook, or spaces between
                                    valid = False
                                    break
                        if(valid == False):
                            break
                    if(valid == False):
                        break
                
                if(valid == True): 
                    self.legalMoves.append([0,0]) #can move to left rook
            #right rook
            if((board[0][7].name == "wR" and board[0][7].hasMoved == False) and board[0][4].name == "." and board[0][5].name == "." and board[0][6].name == "."):
                    valid = True
                    positions = [[0,7], [0,6], [0,5], [0,4], [0, 3]]
                    for y in range(0,8):
                        for x in range(0,8):
                            if(board[y][x].colour == 1): #if the piece is black
                                for attack in board[y][x].legalMoves:
                                    if(attack in positions): #if a piece of the opposite colour is attacking either the king, rook, or spaces between
                                        valid = False
                                        break
                            if(valid == False):
                                break
                        if(valid == False):
                            break
                    
                    if(valid == True):
                        self.legalMoves.append([0,7]) #can move to right rook
                        
        elif(self.hasMoved == False and self.colour == 1): #black king
            #left rook
            if((board[7][0].name == "bR" and board[7][0].hasMoved == False) and board[7][1].name == "." and board[7][2].name == "."):
                valid = True
                positions = [[7,0], [7,1], [7,2], [7,3]]
                for y in range(0,8):
                    for x in range(0,8):
                        if(board[y][x].colour == 0): #if the piece is white
                            for attack in board[y][x].legalMoves:
                                if(attack in positions): #if a piece of the opposite colour is attacking either the king, rook, or spaces between
                                    valid = False
                                    break
                        if(valid == False):
                            break
                    if(valid == False):
                        break
                
                if(valid == True): 
                    self.legalMoves.append([7,0]) #can move to left rook
            #right rook
            if((board[7][7].name == "bR" and board[7][7].hasMoved == False) and board[7][4].name == "." and board[7][5].name == "." and board[7][6].name == "."):
                    valid = True
                    positions = [[0,7], [0,6], [0,5], [0,4], [0, 3]]
                    for y in range(0,8):
                        for x in range(0,8):
                            if(board[y][x].colour == 0): #if the piece is white
                                for attack in board[y][x].legalMoves:
                                    if(attack in positions): #if a piece of the opposite colour is attacking either the king, rook, or spaces between
                                        valid = False
                                        break
                            if(valid == False):
                                break
                        if(valid == False):
                            break
                    
                    if(valid == True):
                        self.legalMoves.append([0,7]) #can move to right rook
        
            
        if(conf == True and AIMove == False): 
            newLegals = copy(self.legalMoves)
            for i in self.legalMoves: #confirms that legal moves will not allow a the king to be in check after being made
                isChecked = self.confirmLegalMove(board, i) #passes each move into confirmLegalMove function
                if(isChecked == True):
                    newLegals.remove(i)
            self.legalMoves = copy(newLegals)
            
    # Returns true if the kind is in check
    def checkCheck(self):
        if(len(self.attackedBy) > 0):
            self.isChecked = True
            return True
        else:
            self.isChecked = False
            return False
