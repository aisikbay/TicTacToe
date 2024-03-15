# TIC TAC TOE
# Aram Isikbay
# *Please use VSCode for testing: the UI color is designed with the VSCode terminal in mind.

# random used to make computer choices different each time when only the type of choice matters (side, corner, center)
import random

sideLength = 3
totalLength = sideLength**2

def printBoard(b):
    GRAY = '\033[30m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    ENDC = '\033[m'
    for i in range(totalLength):
        print(' ', end="")
        # If a spot is free, print the index number in gray else print the marker in its color
        if b[i] == None:
            print(GRAY + str(i) + ENDC, end="")
        elif b[i] == 'X':
            print(RED + b[i] + ENDC, end="")
        elif b[i] == 'O':
            print(BLUE + b[i] + ENDC, end="")
        # Special cases for end of row formatting
        if i % sideLength + 1 != sideLength:
            #Keep cell spacing consistent
            if i < 10 or b[i] != None:
                print(' ', end="")
            print('|', end="")
        elif i != totalLength - 1:
            print('\n' + '-' * (sideLength * 4 - 1))
    print("\n")

def checkWin(b, p):
    # Horizontals and verticals
    for i in range(sideLength):
        if all(b[i * sideLength + j] == p for j in range(sideLength)) or all(b[j * sideLength + i] == p for j in range(sideLength)):
            return True
    # Diagonals
    if all(b[i * sideLength + i] == p for i in range(sideLength)) or all(b[i * sideLength + sideLength - i - 1] == p for i in range(sideLength)):
        return True
    return False

def checkDraw(b):
    for i in b:
        if i is None:
            return False
    return True

def testWinningMove(b, player, cell):
    boardCopy = b.copy()
    boardCopy[cell] = player
    return checkWin(boardCopy, player)

def testForkingMove(b, player, cell):
    boardCopy = b.copy()
    boardCopy[cell] = player
    winningMoves = 0
    for j in range(totalLength):
        if boardCopy[j] is None and testWinningMove(boardCopy, player, j):
            winningMoves += 1
    return winningMoves > 1

def computerMove(b, computerMark, playerMark):
    # Check for moves that will make computer win
    for cell in range(totalLength):
        if b[cell] is None and testWinningMove(b, computerMark, cell):
            return cell
    # Check for moves to block player from winning
    for cell in range(totalLength):
        if b[cell] is None and testWinningMove(b, playerMark, cell):
            return cell
    # Check computer forking opportunity
    for cell in range(totalLength):
        if b[cell] is None and testForkingMove(b, computerMark, cell):
            return cell
    # Check player forking opportunity, count potential forks
    forks = 0
    for cell in range(totalLength):
        if b[cell] is None and testForkingMove(b, playerMark, cell):
            forks += 1
            tempMove = cell
    if forks == 1:
        return tempMove
    # If there is more than one fork the player can use, force the player to block computer win by choosing a side
    elif forks == 2:
        for cell in sides:
            if b[cell] is None:
                return cell
    centers = []
    if sideLength == 3:
        centers.append(totalLength // 2)
    else:
        for i in range(1, sideLength - 1):
            centers.extend(range(i * sideLength + 1, (i + 1) * sideLength - 1))
        random.shuffle(centers)
    for cell in centers:
        if b[cell] is None:
            return cell
        
    corners = []
    for i in range(2):
        for j in range(2):
            row = i * (sideLength - 1)
            col = j * (sideLength - 1)
            corners.append(row * sideLength + col)
    random.shuffle(corners)
    for cell in corners:
        if b[cell] is None:
            return cell
        
    sides = []
    sides.extend(range(1, sideLength - 1))
    for i in range(1, sideLength - 1):
        sides.append(i * sideLength)
        sides.append((i + 1) * sideLength - 1)
    sides.extend(range((sideLength - 1) * sideLength + 1, totalLength - 1))
    random.shuffle(sides)
    for cell in sides:
        if b[cell] is None:
            return cell

def computerTurn(board, computerMark, playerMark):
    cell = computerMove(board, computerMark, playerMark)
    board[cell] = computerMark
    print('Computer move: ' + str(cell))

def checkEnd(board, activeMark, playerMark):
    if checkWin(board, activeMark):
        printBoard(board)
        if activeMark == playerMark:
            print('You won!\n')
        else:
            print('You lost\n')
        return True

    if checkDraw(board):
        printBoard(board)
        print('It was a draw!\n')
        return True
    return False

def playerTurn(board, playerMark):
    printBoard(board)
    validInput = False
    while not validInput:
        cellStr = input('Your move (0-{}): '.format(totalLength-1))
        try:
            cell = int(cellStr)
        except ValueError:
            print('Invalid move')
            continue
        if cell not in range(totalLength):
            print('Please choose a spot 0-{}.'.format(totalLength-1))
            continue
        if board[cell] != None:
            print('Spot is taken.')
            continue
        validInput = True
        board[cell] = playerMark

def main():
    gameLoop = True
    print("Welcome! ", end="")
    while gameLoop:
        activeMark = 'X' # X traditionally goes first
        inGame = True
        board = [None] * totalLength
        print("Press ENTER to exit.")
        playerMark = input("Will you play as X or O? (X/O) ")
        if not playerMark:
            inGame = False
            gameLoop = False
        elif playerMark == 'X':
            computerMark = 'O'
        elif playerMark == 'O':
            computerMark = 'X'
        else:
            print('Please choose X or O.\n')
            continue

        while inGame:
            if activeMark == playerMark:
                playerTurn(board, playerMark)
            else:
                computerTurn(board, computerMark, playerMark)
            if checkEnd(board, activeMark, playerMark):
                inGame = False
            if activeMark == 'X':
                activeMark = 'O'
            else:
                activeMark = 'X'

if __name__ == "__main__":
    main()