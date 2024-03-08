# TIC TAC TOE
# Aram Isikbay
# *Please use VSCode for testing: the UI color is designed with the VSCode terminal in mind.

# PLAYER is X
# COMPUTER is O
# Board layout
#  0 | 1 | 2
# -----------
#  3 | 4 | 5
# -----------
#  6 | 7 | 8

# random used to make computer choices different each time
# when only the type of choice matters (side, corner)
import random

def printBoard(b):
    # Color codes
    GRAY = '\033[30m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    # End code
    ENDC = '\033[m'
    for i in range(9):
        print(' ', end="")
        # If a spot is free, print the index in gray.
        # Otherwise print the marker in that player's color
        if b[i] == None:
            print(GRAY + str(i) + ENDC, end="")
        elif b[i] == 'X':
            print(RED + b[i] + ENDC, end="")
        elif b[i] == 'O':
            print(BLUE + b[i] + ENDC, end="")
        # Special cases for end of row formatting
        if i not in [2, 5, 8]:
            print(' |', end="")
        elif i != 8:
            print('\n-----------')
    print("\n")

# Check if player p has three cells in a row on board b
def checkWin(b, p):
    # Check horizontals and verticals (six winning cases)
    for i in range(3):
        if all(b[i * 3 + j] == p for j in range(3)) or all(b[j * 3 + i] == p for j in range(3)):
            return True
    # Check diagonals (two winning cases)
    if (b[0] == p and b[4] == p and b[8] == p) or (b[2] == p and b[4] == p and b[6] == p):
        return True
    # There are no winning conditions of player p
    return False

# Checks if the board is full (after the check of no winning condition)
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
    for j in range(9):
        if boardCopy[j] is None and testWinningMove(boardCopy, player, j):
            winningMoves += 1
    return winningMoves > 1

def computerMove(b):
    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    center = 4
    random.shuffle(corners)
    random.shuffle(sides)
    # Check for moves that will make computer win
    for cell in range(9):
        if b[cell] is None and testWinningMove(b, 'O', cell):
            return cell
    # Check for moves to block player from winning
    for cell in range(9):
        if b[cell] is None and testWinningMove(b, 'X', cell):
            return cell
    # Check computer forking opportunity
    for cell in range(9):
        if b[cell] is None and testForkingMove(b, 'O', cell):
            return cell
    # Check player forking opportunity, count potential forks
    forks = 0
    for cell in range(9):
        if b[cell] is None and testForkingMove(b, 'X', cell):
            forks += 1
            tempMove = cell
    if forks == 1:
        return tempMove
    # If there is more than one fork the player can use
    # Force the player to block computer win by choosing a side
    elif forks == 2:
        for cell in sides:
            if b[cell] is None:
                return cell
    # Pick the center
    if b[center] is None:
        return center
    # Pick any corner
    for cell in corners:
        if b[cell] is None:
            return cell
    # Pick any side
    for cell in sides:
        if b[cell] is None:
            return cell

def main():
    gameLoop = True
    print("Welcome! ", end="")
    while gameLoop:
        playerMark = 'O' # computer goes first by default
        inGame = True
        board = [None] * 9
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
                cellStr = input("Your move (0-8): ")

                # Invalid input (not an integer)
                try:
                    cell = int(cellStr)
                except ValueError:
                    print('Invalid move')
                    continue
                # Spot is out of range
                if cell > 8 or cell < 0:
                    print('Please choose a spot 0-8.')
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