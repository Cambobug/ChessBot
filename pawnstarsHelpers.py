import pieces as p

def letterToNum(letter): #used to convert letters to numbers from player input
    
    if(letter == "A"):
        return 0
    elif(letter == "B"):
        return 1
    elif(letter == "C"):
        return 2
    elif(letter == "D"):
        return 3
    elif(letter == "E"):
        return 4
    elif(letter == "F"):
        return 5
    elif(letter == "G"):
        return 6
    elif(letter == "H"):
        return 7
    else:
        return -1
    
def getKings(board):
    whiteKing = None
    blackKing = None

    for y in range(0, 8):
        for x in range(0,8):
            if(board[y][x].name == "wK"):
                whiteKing = board[y][x]
            if(board[y][x].name == "bK"):
                blackKing = board[y][x]

    return whiteKing, blackKing
            
    