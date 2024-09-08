# packages
from copy import deepcopy
from mcts import *
import time
import random
X, O, EMPTY = 'X', 'O', None
BOARD_SIZE = 5
player2sign = {1:X, -1:O}

# Five_tigers board class
class Board():  # must contain (scores,player,board,valid actions,move) for mcts
    # create constructor (init board class instance)
    def __init__(self, board=[[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]):
        # define players
        self.player = 1
        self.board = deepcopy(board)
        self.scores = [0, 0]
        self.left = 25

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
        # create new board instance that inherits from the current state
        next_state = Board(self.board)
        
        # make move
        next_state.board[row][col] = player2sign[self.player]
        next_state.left = self.left - 1

        # update scores
        next_state.scores = self.scores.copy()
        next_state.update_score(action)

        # swap players
        next_state.player = -self.player
    
        # return new board state
        return next_state
        
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
        
        # return the list of available actions (tuple)
        return actions
    
class Fiver_tigers():
    def __init__(self, board = Board()):
        self.state = board
        self.board = self.state.board
        self.winner = None
        self.player = self.state.player
        self.left = self.state.left
        self.scores = self.state.scores

    def available_actions(self):
        return self.state.generate_actions()
    
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

    def move(self, action):
        self.state = self.state.move(action)
        self.board = self.state.board
        self.player = -self.player
        self.left = self.state.left
        self.scores = self.state.scores
        if self.left == 0:
            self.winner = self.state.check_winner() 

# main game loop
def game_loop(human_player=None):
    print('\n Play Fiver_tigers with AI based on MCTS\n')
    
    if human_player is None:
        human_player = random.choice([-1,1])
    
    # create MCTS instance
    mcts = MCTS()

    game = Fiver_tigers()        
    
    # game loop
    while True:
        game.render()
        available_actions = game.available_actions()  # list containing tuple(i, j)

        # get user input
        if game.player == human_player:
            print("Your Turn")
            while True:
                row = int(input("Choose Row: "))
                column = int(input("Choose Column: "))
                if (row, column) in available_actions:
                    action = (row, column)
                    break
                print("Invalid move, try again.")

        else:
            print("AI's Turn")
            action = mcts.search(game.state) # tuple(i, j)
            if game.left < 15:
                time.sleep(1)
            row, column = action
            print(f"AI chose to move row {row}, column {column}.")
    
        game.move(action)

        # check if the game is won
        if game.winner is not None:
            game.render()
            print()
            print("GAME OVER")
            if game.winner == human_player:
                print(f"Winner is human")
            elif game.winner == -human_player:
                print(f"Winner is AI")
            else:
                print("Tie")
            print('scores:')
            print(f'Human:{game.scores[int((1-human_player)/2)]}')
            print(f'AI:{game.scores[1-int((1-human_player)/2)]}')
            return

    
        


# main driver
if __name__ == '__main__':
    # create board instance
    game_loop(1)
        
        
        
    
    
    
    
    
