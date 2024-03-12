# TIC TAC TOE
# Aram Isikbay
# *Please use VSCode for testing: the UI color is designed with the VSCode terminal in mind.

# PLAYER is X
# COMPUTER is O
# Board layout

# random used to make computer choices different each time
# when only the type of choice matters (side, corner, center)
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

# Tests if a move will win the game
def testWinningMove(b, player, cell):
    boardCopy = b.copy()
    boardCopy[cell] = player
    return checkWin(boardCopy, player)

# Tests if a move will create a forking opportunity
def testForkingMove(b, player, cell):
    boardCopy = b.copy()
    boardCopy[cell] = player
    winningMoves = 0
    for j in range(totalLength):
        if boardCopy[j] is None and testWinningMove(boardCopy, player, j):
            winningMoves += 1
    return winningMoves > 1

def computerMove(b):
    corners = []
    for i in range(2):
        for j in range(2):
            row = i * (sideLength - 1)
            col = j * (sideLength - 1)
            corners.append(row * sideLength + col)

    sides = []
    sides.extend(range(1, sideLength - 1))
    for i in range(1, sideLength - 1):
        sides.append(i * sideLength)
        sides.append((i + 1) * sideLength - 1)
    sides.extend(range((sideLength - 1) * sideLength + 1, totalLength - 1))
        
    centers = []
    if sideLength == 3:
        centers.append(totalLength // 2)
    else:
        for i in range(1, sideLength - 1):
            centers.extend(range(i * sideLength + 1, (i + 1) * sideLength - 1))

    random.shuffle(corners)
    random.shuffle(sides)
    random.shuffle(centers)

    # Check for moves that will make computer win
    for cell in range(totalLength):
        if b[cell] is None and testWinningMove(b, 'O', cell):
            return cell
    # Check for moves to block player from winning
    for cell in range(totalLength):
        if b[cell] is None and testWinningMove(b, 'X', cell):
            return cell
    # Check computer forking opportunity
    for cell in range(totalLength):
        if b[cell] is None and testForkingMove(b, 'O', cell):
            return cell
    # Check player forking opportunity, count potential forks
    forks = 0
    for cell in range(totalLength):
        if b[cell] is None and testForkingMove(b, 'X', cell):
            forks += 1
            tempMove = cell
    if forks == 1:
        return tempMove
    # If there is more than one fork the player can use, force the player to block computer win by choosing a side
    elif forks == 2:
        for cell in sides:
            if b[cell] is None:
                return cell
    for cell in centers:
        if b[cell] is None:
            return cell
    for cell in corners:
        if b[cell] is None:
            return cell
    for cell in sides:
        if b[cell] is None:
            return cell

def main():
    gameLoop = True
    print("Welcome! ", end="")
    while gameLoop:
        playerMark = 'O' # computer goes first by default
        inGame = True
        board = [None] * totalLength
        print("Press ENTER to exit.")
        orderTurn = input("Will you go first or second? (1/2) ")
        # EXIT
        if not orderTurn:
            inGame = False
            gameLoop = False
        elif orderTurn == '1':
            playerMark = 'X'
            printBoard(board)
        # Handle invalid input
        elif orderTurn != '2':
            print('Please choose 1 or 2.\n')
            continue

        while inGame:
            # Player's turn
            if playerMark == 'X':
                cellStr = input('Your move (0-{}): '.format(totalLength-1))
                # Invalid input (not an integer)
                try:
                    cell = int(cellStr)
                except ValueError:
                    print('Invalid move')
                    continue
                # Spot is out of range
                if cell not in range(totalLength):
                    print('Please choose a spot 0-{}.'.format(totalLength-1))
                    continue
                # Spot is taken
                if board[cell] != None:
                    print('Spot is taken.')
                    continue

            # Computer's turn
            else:
                cell = computerMove(board)
                print('Computer move: ' + str(cell))

            # Board is marked
            board[cell] = playerMark

            if checkWin(board, playerMark):
                inGame = False
                printBoard(board)
                if playerMark == 'X':
                    print('You won!\n')
                else:
                    print('You lost\n')
                continue

            if checkDraw(board):
                inGame = False
                printBoard(board)
                print('It was a draw!\n')
                continue

            # Players switch turns
            if playerMark == 'X':
                playerMark = 'O'
            else:
                printBoard(board)
                playerMark = 'X'

if __name__ == "__main__":
    main()