"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]:
        return X
    else:
        xCount = 0
        oCount = 0
        for row in board:
            for cell in row:
                if cell == X:
                    xCount+=1
                elif cell == O:
                    oCount +=1
        if xCount > oCount:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionsSet = set()
    for i in range (0, 3):
        for j in range (0, 3):
            if board[i][j] == EMPTY:
                actionsSet.add((int(i), int(j)))
    return actionsSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if board[action[0]][action[1]] == EMPTY:
        temp = copy.deepcopy(board)
        temp[action[0]][action[1]] = player(temp)
        return temp
    else: 
        raise Exception("That isn't a valid move.")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0] == [X, X, X] or board[1] == [X, X, X] or board[2] == [X, X, X]:
        return X
    elif board[0] == [O, O, O] or board[1] == [O, O, O] or board[2] == [O, O, O]:
        return O
    elif (board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X
    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O
    elif (board[0][0] == X and board[1][0] == X and board[2][0] == X) or (board[0][1] == X and board[1][1] == X and board[2][1] == X) or (board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return X
    elif (board[0][0] == O and board[1][0] == O and board[2][0] == O) or (board[0][1] == O and board[1][1] == O and board[2][1] == O) or (board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return maxPlay(board, actions(board))[1]
    else:
        return minPlay(board, actions(board))[1]

def maxPlay(board, actionsSet):
    if terminal(board):
        return (utility(board), None)

    actionsOrdered = {}

    for action in actionsSet:
        newBoard = result(board, action)
        score = minPlay(newBoard, actions(newBoard))[0]
        actionsOrdered[score] = action
        if score==1:
            break
    
    return sorted(actionsOrdered.items())[-1]

def minPlay(board, actionsSet):
    if terminal(board):
        return (utility(board), None)

    actionsOrdered = {}

    for action in actionsSet:
        newBoard = result(board, action)
        score = maxPlay(newBoard, actions(newBoard))[0]
        actionsOrdered[score] = action
        if score==-1:
            break

    return sorted(actionsOrdered.items())[0]
