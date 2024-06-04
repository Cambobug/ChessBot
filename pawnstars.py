import pieces as p
import pawnstarsHelpers as pH
from copy import deepcopy
import random as r

MAX, MIN = 10000, -10000

def createGrid(board, playerColour, printCheck): # function creates a board and gets all of the updated moves on the board
    numMoves = 0
    if(playerColour == 1): #black
        for y in range(0, 9): #prints the board from blacks perspective
            if(y != 8):
                if(printCheck == True):
                    print(str(y + 1), end = "     ")
                for x in range(0, 8):
                    if(board[y][x].name == "."):
                        if(printCheck == True):
                            print(str(board[y][x].name), end = "      ")
                    else:
                        if(printCheck == True):
                            print(str(board[y][x].name), end = "     ") 
                             
                        board[y][x].getLegalMoves(board, True, False)   #calculates new legal moves
                        numMoves += len(board[y][x].legalMoves)  
            else:
                if(printCheck == True):
                    print("      H      G      F      E      D      C      B      A")
            if(printCheck == True):
                print("\n")
        #print("Black Moves")
        #print(numMoves)
    else:
        for y in range(7, -2, -1): #w prints the board from whites perspective
            if(y != -1):
                if(printCheck == True):
                    print(str(y + 1), end = "     ")
                for x in range(7, -1, -1):
                    if(board[y][x].name == "." and y > -1):
                        if(printCheck == True):
                            print(str(board[y][x].name), end = "      ")
                    else:
                        if(printCheck == True):
                            print(str(board[y][x].name), end = "     ")
                             
                        board[y][x].getLegalMoves(board, True, False) #calculates new legal moves  
                        numMoves += len(board[y][x].legalMoves)
            else:
                if(printCheck == True):
                    print("      A      B      C      D      E      F      G      H")
            if(printCheck == True):
                print("\n")
        #print("White Moves")
        #print(numMoves)
    
                        
def playerMove(board, playerColour): #function takes in a players input an attempts to make the move
    validMove = False
    while(validMove == False):
        if(playerColour == 0): #white
            print("WHITE TO PLAY")
        elif(playerColour == 1): #black
            print("BLACK TO PLAY")
            
        move = input("Input move: ")
        try:
            parsedMove = move.split(" ")
            selectedPieceInput = parsedMove[0]
            moveToInput = parsedMove[1]
            
            if(playerColour == 0): #parses out player input if player is white
                selectedPieceCoord = [int(selectedPieceInput[1]) - 1, 7 - pH.letterToNum(selectedPieceInput[0])]
                moveToCoord = [int(moveToInput[1]) - 1, 7 - pH.letterToNum(moveToInput[0])]
            else: #parses out player input if player is black
                selectedPieceCoord = [int(selectedPieceInput[1]) - 1, 7 -  pH.letterToNum(selectedPieceInput[0])]
                moveToCoord = [int(moveToInput[1]) - 1, 7 -  pH.letterToNum(moveToInput[0])]
             
            selectedPiece = board[selectedPieceCoord[0]][selectedPieceCoord[1]] #gets the selected piece
            if(selectedPiece.colour == playerColour): # makes sure piece being selected is the players piece
                try:
                    ind = selectedPiece.legalMoves.index(moveToCoord)
                    selectedPiece.makeMove(board, ind, deadPieces, False)   
                    validMove = True
                    
                except:
                    print("Selected piece cannot move to selected location!")
            else:
                print("Selected piece is not owned by you or does not exist!")
        except:
            print("Invalid Input!")
            
def gameEndCheck(board, currentPlayerColour, printCheck): # function checks if a board is in stalemate or checkmate
    
    king = None
    numPieces = []
    numLegalMoves = 0
    #gets the number of legal moves as well as the kings
    for y in range(0, 8): 
        for x in range(0, 8):
            # checks that there are pieces on the board other than kings
            if(board[y][x].name != "."):
                numPieces.append(board[y][x])
            if(board[y][x].colour == currentPlayerColour):
                numLegalMoves += len(board[y][x].legalMoves)
                # gets the king pieces
                if(currentPlayerColour == 0 and board[y][x].name == "wK"):
                    king = board[y][x]
                elif(currentPlayerColour == 1 and board[y][x].name == "bK"):
                    king = board[y][x]

    if(numLegalMoves == 0):
        mate = king.checkCheck()
        if(mate == True): #checkmate
            if(currentPlayerColour == 0): #white loss
                if(printCheck == True):
                    print("BLACK WINS BY CHECKMATE")
                return True
            elif(currentPlayerColour == 1): #black loss
                if(printCheck == True):
                    print("WHITE WINS BY CHECKMATE")
                return True
        else: #stalemate
            if (printCheck == True):
                print("STALEMATE")
            return True
    # if there are only kings on the board
    if(len(numPieces) == 2):
        if(printCheck == True): 
            print("2 KINGS STALEMATE")
        return True
    return False

def boardScore(board, AIcolour): #function gets the score of a given board, depending on the colour of the AI
    totalScore = 0
    
    for y in range(0, 8):
        for x in range(0, 8):
            if(board[y][x].colour != -1 and board[y][x].colour != AIcolour): #player piece
                playerKing = None
                currPlayerPiece = board[y][x]
                
                if(isinstance(currPlayerPiece, p.King) == True):
                    playerKing = currPlayerPiece
                    if(playerKing.checkCheck == True): # if the players king is in check
                        if(gameEndCheck(board, playerKing.colour, False) == True): # if the players king is in checkmate 
                            totalScore += 100
                        totalScore += 15
            
                totalScore += len(currPlayerPiece.attackedBy) * currPlayerPiece.value #add to score the value of piece * number of attackers
                totalScore -= currPlayerPiece.value * 2 #subtract from the score the value of the alive player piece
            elif(board[y][x].colour != -1 and board[y][x].colour == AIcolour): #AI piece
                AIKing = None
                currAIPiece = board[y][x]
                
                if(isinstance(currAIPiece, p.King) == True):
                    AIKing = currAIPiece
                    if(AIKing.checkCheck == True): #if the AI's king is in check
                        totalScore -= 100
                    
                totalScore -= len(currAIPiece.attackedBy) * currAIPiece.value * 2 # subtract the value of the AI piece multiplied by the number of times it is being attacked to he score
                totalScore += currAIPiece.value # add the value of the AI piece to the score
                
    return totalScore
                
def createHypoBoard(board, pieceMoving, move, AIMove): #function creates a hypothetical board off of a given board and move
    hypoBoard = []
    hypoDeads = []
    
    #copy given board and everythin inside (as to not affect our true current board)
    for row in range(0, 8):
            hypoBoard.append([])
            for i in range(0, 8):
                hypoBoard[row].append(deepcopy(board[row][i]))
    
    hypoPiece = hypoBoard[pieceMoving.positionY][pieceMoving.positionX]
    moveNum = hypoPiece.legalMoves.index(move)
    hypoPiece.makeMove(hypoBoard, moveNum, hypoDeads, True) #make the move that is being examined on nextboard
    #checks if the piece moved was a pawn and if it was to be promoted
    if(isinstance(hypoPiece, p.Pawn)):
        if(hypoPiece.colour == 0 and hypoPiece.positionY == 7):
            hypoBoard[hypoPiece.positionY][hypoPiece.positionX] = hypoPiece.promotion(True)
            deadPieces.append(hypoPiece)
        elif(hypoPiece.colour == 1 and hypoPiece.positionY == 0):
            hypoBoard[hypoPiece.positionY][hypoPiece.positionX] = hypoPiece.promotion(True)
            deadPieces.append(hypoPiece)


    #calculate all legal moves on hypoboard
    for y in range(0, 8):
        for x in range(0, 8):
            if(hypoBoard[y][x].name != "."):
                hypoBoard[y][x].getLegalMoves(hypoBoard, True, AIMove)
        
    p.calculateAttackedBy(hypoBoard)
    
    return hypoBoard


def minMaxTree(currDepth, maxDepth, AIcolour, parentBoard, AITurn, alpha, beta): #function uses a min max tree to decide what moves to make from the given board (AI ALGORITHM)
       
    if(currDepth == maxDepth): #if we are at the maximum depth of the tree
        return boardScore(parentBoard, AIcolour)
    else: #check if the game is over
        if(gameEndCheck(parentBoard, AIcolour, False) == True): #if AI lost
            return -1500
        else: #if AI wins
            if(AIcolour == 0 and (gameEndCheck(parentBoard, 1, False) == True)): 
                return 1500
            if(AIcolour == 1 and (gameEndCheck(parentBoard, 0, False) == True)):
                return 1500
            
    # CHECK IF KING IS IN CHECK AND IF THEY ARE RETURN SCORE OF BOARD !!!!!!!!!!
    whiteKing, blackKing = pH.getKings(parentBoard)
    
    if(whiteKing == None or blackKing == None):
        print("-----------ERROR-------------")
        print(currDepth)
        print(AIcolour)
        createGrid(parentBoard, 0, True)
        print("-----------------------------")

    if(currDepth > 0):
        if(AIcolour == 0): #white
            if(whiteKing.checkCheck() == True):
                return -1000
            if(blackKing.checkCheck() == True):
                return 1000
        elif(AIcolour == 1): #black
            if(whiteKing.checkCheck() == True):
                return 1000
            if(blackKing.checkCheck() == True):
                return -1000

    if(AITurn): #AI's MOVE
        best = MIN
        possibleBoardScores = []
        parentBoards = []
        for x in range(0, 8):
            for y in range(0, 8):
                if(parentBoard[y][x].colour != -1 and parentBoard[y][x].colour == AIcolour): #look at AI's pieces
                    currPiece = parentBoard[y][x]
                    for i in currPiece.legalMoves: #for each legal move by the AI's piece
                        #if the move being looked does not kill the king
                        if((currDepth == 0) or (whiteKing.checkCheck == True) or (blackKing.checkCheck == True)):
                            hypoBoard = createHypoBoard(parentBoard, currPiece, i, False) #creates a hypothetical board
                        else:
                            hypoBoard = createHypoBoard(parentBoard, currPiece, i, True)

                        if(currDepth == 0): #if we are at the first layer below our current board
                            parentBoards.append(hypoBoard) #store the boards in our parentBoards
                        
                        score = minMaxTree(currDepth + 1, maxDepth, AIcolour, hypoBoard, False, alpha, beta)
                        
                        if(currDepth == 0): #if we are at the first layer below our current board
                            possibleBoardScores.append(score) #store the scores of hypoBoard in same order as our parentBoards
                        
                        best = max(best, score)
                        alpha = max(alpha, best)
                        
                        if(beta <= alpha):
                            break
                        
                if(beta <= alpha):
                    break
            if(beta <= alpha):
                break
        
        if(currDepth > 0): #if we are at the first layer below our current board
            return best
        elif(currDepth == 0): # return the board that has the best outcome down the tree
            bestScore = max(possibleBoardScores)
            bestPossibleBoards = []
            for i in range(0, len(possibleBoardScores)):
                if((possibleBoardScores)[i] == bestScore):
                    bestPossibleBoards.append(parentBoards[i])
                    
            ranIndex = r.randint(0, len(bestPossibleBoards) - 1)
            parentBoardIndex = parentBoards.index(bestPossibleBoards[ranIndex])
            return parentBoards[parentBoardIndex]
            
    else: #PLAYERS MOVE
        best = MAX
        possibleBoardScores = []
        parentBoards = []
        for x in range(0, 8):
            for y in range(0, 8):
                if(parentBoard[y][x].colour != -1 and parentBoard[y][x].colour != AIcolour): #look at players pieces
                    currPiece = parentBoard[y][x]
                    for i in currPiece.legalMoves: #for each legal move by the players pieces
                        if((whiteKing.checkCheck == True) or (blackKing.checkCheck == True)):
                            hypoBoard = createHypoBoard(parentBoard, currPiece, i, False) # create a new board off of the move being looked at by currpiece
                        else:
                            hypoBoard = createHypoBoard(parentBoard, currPiece, i, True)
                            
                        #pass hypoboard into minMaxTree function which will create more boards off of hypoBoard, ultimately arriving at the bottom of the tree
                        score = minMaxTree(currDepth + 1, maxDepth, AIcolour, hypoBoard, True, alpha, beta) # worst board is passed back
                        
                        best = min(best, score)
                        beta = min(beta, best)
                        
                        if(beta <= alpha):
                            break
                        
                if(beta <= alpha):
                    break
            if(beta <= alpha):
                break
        
        return best

        
#creates peices 
Br1 = p.Rook('bR', 1, 0, 7)
Br2 = p.Rook('bR', 1, 7, 7)
Bn1 = p.Knight('bN', 1, 1, 7)
Bn2 = p.Knight('bN', 1, 6, 7)
Bb1 = p.Bishop('bB', 1, 2, 7)
Bb2 = p.Bishop('bB', 1, 5, 7)
Bq1 = p.Queen('bQ', 1, 4, 7)
Bk = p.King('bK', 1, 3, 7)
Bp1 = p.Pawn('bP', 1, 0, 6)
Bp2 = p.Pawn('bP', 1, 1, 6)
Bp3 = p.Pawn('bP', 1, 2, 6)
Bp4 = p.Pawn('bP', 1, 3, 6)
Bp5 = p.Pawn('bP', 1, 4, 6)
Bp6 = p.Pawn('bP', 1, 5, 6)
Bp7 = p.Pawn('bP', 1, 6, 6)
Bp8 = p.Pawn('bP', 1, 7, 6)

Wr1 = p.Rook('wR', 0, 0, 0)
Wr2 = p.Rook('wR', 0, 7, 0)
Wn1 = p.Knight('wN', 0, 1, 0)
Wn2 = p.Knight('wN', 0, 6, 0)
Wb1 = p.Bishop('wB', 0, 2, 0)
Wb2 = p.Bishop('wB', 0, 5, 0)
Wq1 = p.Queen('wQ', 0, 4, 0)
Wk = p.King('wK', 0, 3, 0)
Wp1 = p.Pawn('wP', 0, 0, 1)
Wp2 = p.Pawn('wP', 0, 1, 1)
Wp3 = p.Pawn('wP', 0, 2, 1)
Wp4 = p.Pawn('wP', 0, 3, 1)
Wp5 = p.Pawn('wP', 0, 4, 1)
Wp6 = p.Pawn('wP', 0, 5, 1)
Wp7 = p.Pawn('wP', 0, 6, 1)
Wp8 = p.Pawn('wP', 0, 7, 1)

#places pieces in array[y][x]
# h g f e d c b a
pieceArray = [[Wr1,Wn1,Wb1,Wk,Wq1,Wb2,Wn2,Wr2],
              [Wp1,Wp2,Wp3,Wp4,Wp5,Wp6,Wp7,Wp8],
              [p.Empty(), ] * 8,
              [p.Empty(), ] * 8,
              [p.Empty(), ] * 8,
              [p.Empty(), ] * 8,
              [Bp1,Bp2,Bp3,Bp4,Bp5,Bp6,Bp7,Bp8],
              [Br1,Bn1,Bb1,Bk,Bq1,Bb2,Bn2,Br2]]

deadPieces = []
player1 = None

# asks whether the user wants to play 2 player or 1 player
twoPlayer = False
correctInput = False
while(correctInput == False):
    userInput = input("How many players are playing? (1 or 2): ")
    try:
        numPlayers = int(userInput)
        if(numPlayers == 2):
            correctInput = True
        elif(numPlayers == 1):
            correctInput = True
        elif(numPlayers == 0):
            correctInput = True
        else:
            print("Invalid input!")
    except:
        print("Invalid input!")

#if player is playing against the computer, asks what colour the player wants to play
if(numPlayers == 1):
    correctInput = False      
    while(correctInput == False):
        userInput = input("Which colour would you like to play? (Black or White): ")
        if(userInput == "White"):
            player1 = 0
            correctInput = True
        elif(userInput == "Black"):
            player1 = 1
            correctInput = True
        else:
            print("Invalid input!")

# central game loop
gameEnd = False
if(numPlayers == 2 or (numPlayers == 1 and player1 == 0)):
    createGrid(pieceArray, 0, True)
while(gameEnd == False):
    
    if(numPlayers == 2): # two player chess
        playerMove(pieceArray, 0)
        createGrid(pieceArray, 1, True)
        p.calculateAttackedBy(pieceArray)
        gameEnd = gameEndCheck(pieceArray, 1, True)
        if(gameEnd == True):
            break
        
        if(Wk.checkCheck()):
            print("WHITE IN CHECK")
        elif(Bk.checkCheck()):
            print("BLACK IN CHECK")

        playerMove(pieceArray, 1) 
        createGrid(pieceArray, 0, True)
        p.calculateAttackedBy(pieceArray)
        gameEnd = gameEndCheck(pieceArray, 0, True)
        if(gameEnd == True):
            break
        
        if(Wk.checkCheck()):
            print("WHITE IN CHECK")
        elif(Bk.checkCheck()):
            print("BLACK IN CHECK")
                
    elif(numPlayers == 1): #one player chess
        if(player1 == 0): #player is white
            playerMove(pieceArray, 0)
            p.calculateAttackedBy(pieceArray)
            gameEnd = gameEndCheck(pieceArray, 1, True)
            if(gameEnd == True):
                break
            
            if(Wk.checkCheck()):
                print("WHITE IN CHECK")
            elif(Bk.checkCheck()):
                print("BLACK IN CHECK")
            
            pieceArray = minMaxTree(0, 3, 1, pieceArray, True, MIN, MAX) #depth of 3 search for black
            createGrid(pieceArray, 1, False)
            p.calculateAttackedBy(pieceArray)
            gameEnd = gameEndCheck(pieceArray, 0, True)
            if(gameEnd == True):
                break
            
            if(Wk.checkCheck()):
                print("WHITE IN CHECK")
            elif(Bk.checkCheck()):
                print("BLACK IN CHECK")
                
            createGrid(pieceArray, 0, True)
        else: #player is black
            createGrid(pieceArray, 0, False)
            
            pieceArray = minMaxTree(0, 3, 0, pieceArray, True, MIN, MAX) #depth of 3 search for white
            createGrid(pieceArray, 1, True)
            p.calculateAttackedBy(pieceArray)
            gameEnd = gameEndCheck(pieceArray, 1, True)
            if(gameEnd == True):
                break
            
            if(Wk.checkCheck()):
                print("WHITE IN CHECK")
            elif(Bk.checkCheck()):
                print("BLACK IN CHECK")
            

            playerMove(pieceArray, 1) #player move black
            createGrid(pieceArray, 0, False)
            p.calculateAttackedBy(pieceArray)
            gameEnd = gameEndCheck(pieceArray, 0, True)
            if(gameEnd == True):
                break
            
            if(Wk.checkCheck()):
                print("WHITE IN CHECK")
            elif(Bk.checkCheck()):
                print("BLACK IN CHECK")
    elif(numPlayers == 0): # if you want the AI to face eachother
        createGrid(pieceArray, 0, False)
        
        print("-------------------------New Set-----------------------------")
        
        #startTime = time.time()
        pieceArray = minMaxTree(0, 3, 0, pieceArray, True, MIN, MAX) #depth of 3 search for white
        #endTime = time.time()
        
        #totalTime = endTime - startTime
        #print(totalTime)
        
        print("WHITES MOVE")
        createGrid(pieceArray, 1, True) #create grid for black
        p.calculateAttackedBy(pieceArray)
        
        numLegalMoves = 0
        for y in range(0, 8): 
            for x in range(0, 8):
                # checks that there are pieces on the board other than kings
                if(pieceArray[y][x].colour == 1):
                    numLegalMoves += len(pieceArray[y][x].legalMoves)
        
        print("Blacks Legal Moves")        
        print(numLegalMoves)
        
        gameEnd = gameEndCheck(pieceArray, 1, True)
        if(gameEnd == True):
            break
        
        if(Wk.checkCheck()):
                print("WHITE IN CHECK")
        elif(Bk.checkCheck()):
            print("BLACK IN CHECK")
        
        #startTime = time.time()
        pieceArray = minMaxTree(0, 3, 1, pieceArray, True, MIN, MAX) #depth of 3 search for black
        
        #endTime = time.time()
        #totalTime = endTime - startTime
        #print(totalTime)
        
        print("BLACKS MOVE")
        createGrid(pieceArray, 1, True)
        createGrid(pieceArray, 0, False) #create grid for white
        p.calculateAttackedBy(pieceArray)
        
        numLegalMoves = 0
        for y in range(0, 8): 
            for x in range(0, 8):
                # checks that there are pieces on the board other than kings
                if(pieceArray[y][x].colour == 0):
                    numLegalMoves += len(pieceArray[y][x].legalMoves)
        
        print("Whites Legal Moves")        
        print(numLegalMoves)

                    
        gameEnd = gameEndCheck(pieceArray, 0, True)
        if(gameEnd == True):
            break  
        
        if(Wk.checkCheck()):
            print("WHITE IN CHECK")
        elif(Bk.checkCheck()):
            print("BLACK IN CHECK")
            
        
