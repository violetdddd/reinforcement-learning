"""
Five_tigers Player
"""

import math
from copy import deepcopy
import random
import time

X = 1
O = -1
EMPTY = 0
BOARD_SIZE = 5
depth = 8
sort_key = {(0, 0): 22,
            (0, 1): 14,
            (0, 2): 1,
            (0, 3): 15,
            (0, 4): 23,
            (1, 0): 16,
            (1, 1): 5,
            (1, 2): 9,
            (1, 3): 6,
            (1, 4): 17,
            (2, 0): 2,
            (2, 1): 10,
            (2, 2): 13,
            (2, 3): 11,
            (2, 4): 3,
            (3, 0): 18,
            (3, 1): 7,
            (3, 2): 12,
            (3, 3): 8,
            (3, 4): 19,
            (4, 0): 24,
            (4, 1): 20,
            (4, 2): 4,
            (4, 3): 21,
            (4, 4): 25}


class Fiver_tigers():
    def __init__(self, board=[[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]):
        # define players
        self.player = 1
        self.board = deepcopy(board)
        self.scores = [0, 0]
        self.left = 25
        self.winner = None

    def update_score(self, action):
        related = {
            (0, 0): [1, 6, 11, 21, 30, 31, ],
            (0, 1): [1, 7, 13, 22, 31, 32, ],
            (0, 2): [1, 8, 17, 18, 21, 23, 32, 33, ],
            (0, 3): [1, 9, 14, 22, 33, 34, ],
            (0, 4): [1, 10, 12, 23, 30, 34, ],
            (1, 0): [2, 6, 15, 24, 31, 35, ],
            (1, 1): [2, 7, 11, 17, 21, 25, 31, 32, 35, 36, ],
            (1, 2): [2, 8, 13, 14, 22, 24, 26, 32, 33, 36, 37, ],
            (1, 3): [2, 9, 12, 18, 23, 25, 33, 34, 37, 38, ],
            (1, 4): [2, 10, 16, 26, 34, 38, ],
            (2, 0): [3, 6, 17, 20, 21, 27, 35, 39, ],
            (2, 1): [3, 7, 14, 15, 22, 24, 28, 35, 36, 39, 40, ],
            (2, 2): [3, 8, 11, 12, 21, 23, 25, 27, 29, 30, 36, 37, 40, 41, ],
            (2, 3): [3, 9, 13, 16, 22, 26, 28, 37, 38, 41, 42, ],
            (2, 4): [3, 10, 18, 19, 23, 29, 38, 42, ],
            (3, 0): [4, 6, 14, 24, 39, 43, ],
            (3, 1): [4, 7, 12, 20, 25, 27, 39, 40, 43, 44, ],
            (3, 2): [4, 8, 15, 16, 24, 26, 28, 40, 41, 44, 45, ],
            (3, 3): [4, 9, 11, 19, 25, 29, 41, 42, 45, 46, ],
            (3, 4): [4, 10, 13, 26, 42, 46, ],
            (4, 0): [5, 6, 12, 27, 30, 43, ],
            (4, 1): [5, 7, 16, 28, 43, 44, ],
            (4, 2): [5, 8, 19, 20, 27, 29, 44, 45, ],
            (4, 3): [5, 9, 15, 28, 45, 46, ],
            (4, 4): [5, 10, 11, 29, 30, 46, ]
        }
        def add_score(base_sign, score):
            if base_sign == X:
                    self.scores[0] += score
            else:
                    self.scores[1] += score
        def check_raw(base_sign, i):
            if self.board[i][0] == base_sign and self.board[i][1] == base_sign and self.board[i][2] == base_sign and self.board[i][3] == base_sign and self.board[i][4] == base_sign:
                add_score(base_sign,5)
        def check_column(base_sign, i):
            if self.board[0][i] == base_sign and self.board[1][i] == base_sign and self.board[2][i] == base_sign and self.board[3][i] == base_sign and self.board[4][i] == base_sign:
                add_score(base_sign,5)
        def check_5x(base_sign, i):
            if i == 1 and self.board[2][2] == base_sign and self.board[0][0] == base_sign and self.board[1][1] == base_sign and self.board[3][3] == base_sign and self.board[4][4] == base_sign:
                add_score(base_sign,5)
            if i == 2 and self.board[2][2] == base_sign and self.board[0][4] == base_sign and self.board[1][3] == base_sign and self.board[3][1] == base_sign and self.board[4][0] == base_sign:
                add_score(base_sign,5)
        def check_4x(base_sign, i):
            if i == 2 and self.board[0][3] == base_sign and self.board[1][2] == base_sign and self.board[2][1] == base_sign and self.board[3][0] == base_sign:
                add_score(base_sign,4)
            if i == 1 and self.board[0][1] == base_sign and self.board[1][2] == base_sign and self.board[2][3] == base_sign and self.board[3][4] == base_sign:
                add_score(base_sign,4)
            if i == 3 and self.board[4][3] == base_sign and self.board[3][2] == base_sign and self.board[2][1] == base_sign and self.board[1][0] == base_sign:
                add_score(base_sign,4)
            if i == 4 and self.board[4][1] == base_sign and self.board[3][2] == base_sign and self.board[2][3] == base_sign and self.board[1][4] == base_sign:
                add_score(base_sign,4)
        def check_3x(base_sign, i):
            if i == 1 and self.board[0][2] == base_sign and self.board[1][1] == base_sign and self.board[2][0] == base_sign:
                add_score(base_sign,3)
            if i == 2 and self.board[0][2] == base_sign and self.board[1][3] == base_sign and self.board[2][4] == base_sign:
                add_score(base_sign,3)
            if i == 4 and self.board[4][2] == base_sign and self.board[3][1] == base_sign and self.board[2][0] == base_sign:
                add_score(base_sign,3)
            if i == 3 and self.board[4][2] == base_sign and self.board[3][3] == base_sign and self.board[2][4] == base_sign:
                add_score(base_sign,3)
        def check_big5(base_sign):
            if self.board[2][2] == base_sign and self.board[0][0] == base_sign and self.board[4][0] == base_sign and self.board[0][4] == base_sign and self.board[4][4] == base_sign:
                add_score(base_sign,10)
        def check_small5(base_sign, index):
            i, j = index // 3 + 1, index % 3 + 1
            if self.board[i][j] == base_sign and self.board[i-1][j-1] == base_sign and self.board[i-1][j+1] == base_sign and self.board[i+1][j-1] == base_sign and self.board[i+1][j+1] == base_sign:
                add_score(base_sign,5)
        def check_well(base_sign, index):
            i, j = index // 4, index % 4
            if self.board[i][j] == base_sign and self.board[i][j+1] == base_sign and self.board[i+1][j] == base_sign and self.board[i+1][j+1] == base_sign:
                add_score(base_sign,1)
        
        i, j = action
        base_sign = self.board[i][j]
        last_scores = self.scores.copy()
        for index in related[action]:
            if 1 <= index <= 5:
                check_raw(base_sign, index-1)
            elif 6 <= index <= 10:
                check_column(base_sign, index-6)
            elif 11 <= index <= 12:
                check_5x(base_sign, index-10)
            elif 13 <= index <= 16:
                check_4x(base_sign, index-12)
            elif 17 <= index <= 20:
                check_3x(base_sign, index-16)
            elif 21 <= index <= 29:
                check_small5(base_sign, index-21)
            elif index == 30:
                check_big5(base_sign)
            elif 31 <= index <= 46:
                check_well(base_sign, index-31)
        now_scores = self.scores.copy()

        return [now_scores[0]-last_scores[0], now_scores[1]-last_scores[1]]
    
    def check_winner(self):
        if self.scores[0] > self.scores[1]:
            return 1
        elif self.scores[0] < self.scores[1]:
            return -1
        else:
            return 0
            
    # make move
    def move(self, action):
        row, col = action
        
        # make move
        self.board[row][col] = self.player
        self.left = self.left - 1

        # update scores
        add_scores = self.update_score(action)

        # swap players
        self.player = -self.player

        if self.left == 0:
            self.winner = self.check_winner() 
    
        # return new board state
        return add_scores
    
    def recall(self, action, add_scores):
        row, col = action
        
        # make move
        self.board[row][col] = 0
        self.left = self.left + 1

        # update scores
        self.scores[0] -= add_scores[0]
        self.scores[1] -= add_scores[1]

        # swap players
        self.player = -self.player

        self.winner = None
        
    # generate legal moves to play in the current position
    def generate_actions(self):
        # define states list (move list - list of available actions to consider)
        actions = []
        
        # loop over board rows
        for row in range(BOARD_SIZE):
            # loop over board columns
            for col in range(BOARD_SIZE):
                # make sure that current square is empty
                if self.board[row][col] == EMPTY:
                    # append available (row, col) action to list
                    actions.append((row, col))

        actions.sort(key=lambda x: sort_key[x])
        # return the list of available actions (tuple)
        return actions
    
    def render(self):
        print()
        print("board:")
        print("   0 1 2 3 4")
        for i in range(BOARD_SIZE):
            print(i,end="  ")
            for j in self.board[i]:
                print(j if j is not None else '-',end=" ")
            print()
        print()

    def utility(self):
        """
        Returns X_scores - O_scores.
        """
        return self.scores[0] - self.scores[1]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #raise NotImplementedError
    if board.left == 0:
        return None
    if board.left == 24:
        return (4,4)
    def MAX_VALUE(board, depth): 
        if depth == 0 or board.left == 0: 
            return utility(board)
        now_max = float('-inf')
        for action in board.generate_actions(): 
            now_max = max(now_max, MIN_VALUE(board.move(action), depth - 1))
        return now_max
    def MIN_VALUE(board, depth): 
        if depth == 0 or board.left == 0: 
            return utility(board)
        now_min = float('inf')
        for action in board.generate_actions(): 
            now_min = min(now_min, MAX_VALUE(board.move(action), depth - 1))
        return now_min
    
    now_action = None
    if board.player == X:
        max_value = float('-inf')
        for action in board.generate_actions():
            now_value=MIN_VALUE(board.move(action), depth)
            if now_value > max_value:
                max_value = now_value
                now_action = action
            elif now_value == max_value:
                if random.randint(0,1):
                    now_action = action
    else:
        min_value = float('inf')
        for action in board.generate_actions():
            now_value=MAX_VALUE(board.move(action), depth)
            if now_value < min_value:
                min_value = now_value
                now_action = action
            elif now_value == min_value:
                if random.randint(0,1):
                    now_action = action
    return now_action

def ab_minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board.left == 0:
        return None
    def ab_MAX_VALUE(board, depth, alpha, beta): 
        if depth == 0 or board.left == 0: 
            return board.utility()
        
        available_actions = board.generate_actions()
        now_max = float('-inf')
        for action in available_actions: 
            add_scores = board.move(action)
            now_max = board.utility()
            board.recall(action, add_scores)
            if now_max > beta or now_max > 0:
                return now_max 
            
        now_max = float('-inf')
        for action in available_actions:
            add_scores = board.move(action) 
            now_max = max(now_max, ab_MIN_VALUE(board, depth - 1, alpha, beta))
            board.recall(action, add_scores)
            if now_max >= beta or now_max > 0:
                return now_max 
            alpha = max(alpha, now_max)
        return now_max
    
    def ab_MIN_VALUE(board, depth, alpha, beta): 
        if depth == 0 or board.left == 0: 
            return board.utility()
        
        available_actions = board.generate_actions()
        now_min = float('inf')
        for action in available_actions: 
            add_scores = board.move(action) 
            now_min = board.utility()
            board.recall(action, add_scores)
            if now_min < alpha or now_min < 0:
                return now_min 
            
        now_min = float('inf')
        for action in available_actions: 
            add_scores = board.move(action)
            now_min = min(now_min, ab_MAX_VALUE(board, depth - 1, alpha, beta))
            board.recall(action, add_scores)
            if now_min <= alpha or now_min < 0:
                return now_min 
            beta = min(beta, now_min)
        return now_min
    
    alpha, beta = float('-inf'), float('inf')
    now_action = None
    if board.player == X:
        for action in board.generate_actions():
            add_scores = board.move(action)
            now_value=ab_MIN_VALUE(board, depth, alpha, beta)
            board.recall(action, add_scores)
            if now_value > alpha:
                alpha = now_value
                now_action = action
    else:
        for action in board.generate_actions():
            add_scores = board.move(action)
            now_value=ab_MAX_VALUE(board, depth, alpha, beta)
            board.recall(action, add_scores)
            if now_value < beta:
                beta = now_value
                now_action = action
    return now_action

