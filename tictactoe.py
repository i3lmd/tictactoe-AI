"""
Tic Tac Toe Player
"""
from copy import deepcopy as dc
import math


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
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)
    return X if count_X <= count_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    
    row, col = action
    copy_board = dc(board)  # Create deep copy to avoid modifying the original
    copy_board[row][col] = player(board)  # Place the correct player's mark
    
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None  # No winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_result = winner(board)
    if winner_result == X:
        return 1
    elif winner_result == O:
        return -1
    return 0  # Tie


def minimax_value(board, player):
    if terminal(board):
        return utility(board)
    if player == X:
        return max(minimax_value(result(board, action), O) for action in actions(board))
    else:
        return min(minimax_value(result(board, action), X) for action in actions(board))


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    best_action = None

    if current_player == X:
        max_value = float('-inf')
        for action in actions(board):
            value = minimax_value(result(board, action), O)
            if value > max_value:
                max_value = value
                best_action = action
    else:
        min_value = float('inf')
        for action in actions(board):
            value = minimax_value(result(board, action), X)
            if value < min_value:
                min_value = value
                best_action = action

    return best_action