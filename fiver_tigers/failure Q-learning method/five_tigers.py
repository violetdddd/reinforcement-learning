import math
import random
import time
import numpy as np
import copy

X = "X"
O = "O"
EMPTY = None

class five_tigers():

    def __init__(self, initial=[[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]):
        """
        Initialize game board.
        Each game board has
            - `board`: a list of the playing board
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.board = copy.deepcopy(initial)
        self.player = 0
        self.winner = None
        self.left = 25
        self.scores = [0, 0]
        self.scores_added = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    @classmethod
    def available_actions(cls, board):
        """
        five_tigers.available_actions(board) takes a `board` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of make a move in raw_i,column_j
        """
        actions = set()
        for i in range(5) :
            for j in range(5) :
                if board[i][j] == EMPTY :
                    actions.add((i,j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        five_tigers.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = five_tigers.other_player(self.player)

    def now_player_sign(self):
        if self.player == 0:
            return X
        else:
            return O
        
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
        def add_score(base_sign, score, index):
            if base_sign == X:
                    self.scores[0] += score
            else:
                    self.scores[1] += score
            self.scores_added[index-1] += 1
        def check_raw(base_sign, i):
            if self.board[i][0] == base_sign and self.board[i][1] == base_sign and self.board[i][2] == base_sign and self.board[i][3] == base_sign and self.board[i][4] == base_sign:
                add_score(base_sign,5,i+1)
        def check_column(base_sign, i):
            if self.board[0][i] == base_sign and self.board[1][i] == base_sign and self.board[2][i] == base_sign and self.board[3][i] == base_sign and self.board[4][i] == base_sign:
                add_score(base_sign,5,i+6)
        def check_5x(base_sign, i):
            if i == 1 and self.board[2][2] == base_sign and self.board[0][0] == base_sign and self.board[1][1] == base_sign and self.board[3][3] == base_sign and self.board[4][4] == base_sign:
                add_score(base_sign,5,11)
            if i == 2 and self.board[2][2] == base_sign and self.board[0][4] == base_sign and self.board[1][3] == base_sign and self.board[3][1] == base_sign and self.board[4][0] == base_sign:
                add_score(base_sign,5,12)
        def check_4x(base_sign, i):
            if i == 2 and self.board[0][3] == base_sign and self.board[1][2] == base_sign and self.board[2][1] == base_sign and self.board[3][0] == base_sign:
                add_score(base_sign,4,14)
            if i == 1 and self.board[0][1] == base_sign and self.board[1][2] == base_sign and self.board[2][3] == base_sign and self.board[3][4] == base_sign:
                add_score(base_sign,4,13)
            if i == 3 and self.board[4][3] == base_sign and self.board[3][2] == base_sign and self.board[2][1] == base_sign and self.board[1][0] == base_sign:
                add_score(base_sign,4,15)
            if i == 4 and self.board[4][1] == base_sign and self.board[3][2] == base_sign and self.board[2][3] == base_sign and self.board[1][4] == base_sign:
                add_score(base_sign,4,16)
        def check_3x(base_sign, i):
            if i == 1 and self.board[0][2] == base_sign and self.board[1][1] == base_sign and self.board[2][0] == base_sign:
                add_score(base_sign,3,17)
            if i == 2 and self.board[0][2] == base_sign and self.board[1][3] == base_sign and self.board[2][4] == base_sign:
                add_score(base_sign,3,18)
            if i == 4 and self.board[4][2] == base_sign and self.board[3][1] == base_sign and self.board[2][0] == base_sign:
                add_score(base_sign,3,20)
            if i == 3 and self.board[4][2] == base_sign and self.board[3][3] == base_sign and self.board[2][4] == base_sign:
                add_score(base_sign,3,19)
        def check_big5(base_sign):
            if self.board[2][2] == base_sign and self.board[0][0] == base_sign and self.board[4][0] == base_sign and self.board[0][4] == base_sign and self.board[4][4] == base_sign:
                add_score(base_sign,10,30)
        def check_small5(base_sign, index):
            i, j = index // 3 + 1, index % 3 + 1
            if self.board[i][j] == base_sign and self.board[i-1][j-1] == base_sign and self.board[i-1][j+1] == base_sign and self.board[i+1][j-1] == base_sign and self.board[i+1][j+1] == base_sign:
                add_score(base_sign,5,index+21)
        def check_well(base_sign, index):
            i, j = index // 4, index % 4
            if self.board[i][j] == base_sign and self.board[i][j+1] == base_sign and self.board[i+1][j] == base_sign and self.board[i+1][j+1] == base_sign:
                add_score(base_sign,1,index+31)
        
        i, j = action
        base_sign = self.board[i][j]
        for index in related[action]:
            if self.scores_added[index-1] == 0:
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
            return 0
        elif self.scores[0] < self.scores[1]:
            return 1
        else:
            return 2
        
    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        raw, column = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif raw < 0 or raw >= 5 or column < 0 or column >= 5:
            raise Exception("Invalid move")

        # Update board
        self.board[raw][column] = self.now_player_sign()
        self.update_score(action)
        self.switch_player()
        self.left -= 1
        

        # Check for a winner
        if self.left == 0:
            self.winner = self.check_winner()
            


class five_tigersAI():

    def __init__(self, q = dict(), alpha=0.5, epsilon=1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining board, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = q
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = 0.9

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        try :
            return self.q[tuple(state), action]
        except :
            return 0


    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        self.q[tuple(state), action] = old_q + self.alpha * ( reward + self.gamma * future_rewards - old_q )

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        actions = set()
        for i in range(5) :
            for j in range(5) :
                if state[i][j] == EMPTY :
                    actions.add((i,j))
        if len(actions) == 0 :
            return 0
        best = -10000
        for action in actions :
            try :
                best = max(best, self.q[tuple(state), action])
            except :
                best = max(best, 0)
        return best

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        actions = set()
        for i in range(5) :
            for j in range(5) :
                if state[i][j] == EMPTY :
                    actions.add((i,j))
        
        #function of the two posibility
        def bestQ(actions) :
            best = (0, -1000) #(action, Q)pair
            for action in actions :
                try :
                    if best[1] < self.q[tuple(state), action] :
                        best = (action, self.q[tuple(state), action])
                except :
                    if best[1] < 0 :
                        best = (action, 0)
            return best[0]
        def randomQ(actions) :
            repo = list(actions)
            index = np.random.randint(len(repo))
            return repo[index]

        if not epsilon :
            return bestQ(actions)
        
        else :
            choice = np.random.choice([0, 1], p=[self.epsilon, 1-self.epsilon])
            if choice :
                return bestQ(actions)
            else :
                return randomQ(actions)




def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = five_tigersAI()

    def board_to_state(player,copy_state):
        translation = {X:1-player, O:player}
        state = [tuple([translation[j] if j in translation else j for j in copy_state[i]]) for i in range(5)]
        return state
    
    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = five_tigers()
        if 300000 < i < 500000:
            player.epsilon = 0.5
        elif 500000 < i < 700000:
            player.epsilon = 0.3
        elif i > 700000:
            player.epsilon = 0.1
        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None, "add_score": 0},
            1: {"state": None, "action": None, "add_score": 0},
        }

        # Game loop
        while True:

            # Keep track of current state and action
            copy_state = copy.deepcopy(game.board)
            state = board_to_state(game.player, copy_state)
            action = player.choose_action(state)
            

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action
            last_score = game.scores[game.player]


            # Make move
            game.move(action)
            copy_new_state = copy.deepcopy(game.board)
            new_state = board_to_state(game.player, copy_new_state)
            now_score = game.scores[1-game.player]
            last[1-game.player]["add_score"] = now_score - last_score

            # When game is over, update Q values with rewards
            if game.winner is not None:
                new_state_last = board_to_state(1-game.player, copy_new_state)
                if game.winner == 1:
                    player.update(state, action, new_state_last, -20 + last[1-game.player]["add_score"])
                    player.update(
                        last[game.player]["state"],
                        last[game.player]["action"],
                        new_state,
                        10 + last[game.player]["add_score"] - last[1-game.player]["add_score"]
                    )
                elif game.winner == 0:
                    player.update(state, action, new_state_last, 10 + last[1-game.player]["add_score"])
                    player.update(
                        last[game.player]["state"],
                        last[game.player]["action"],
                        new_state,
                        -20 + last[game.player]["add_score"] - last[1-game.player]["add_score"]
                    )
                else:
                    player.update(state, action, new_state_last, -1 + last[1-game.player]["add_score"])
                    player.update(
                        last[game.player]["state"],
                        last[game.player]["action"],
                        new_state,
                        -1 + last[game.player]["add_score"] - last[1-game.player]["add_score"]
                    )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    last[game.player]["add_score"] - last[1-game.player]["add_score"]
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """
    def board_to_state(player,copy_state):
        translation = {X:1-player, O:player}
        state = [tuple([translation[j] if j in translation else j for j in copy_state[i]]) for i in range(5)]
        return state
    
    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = five_tigers()

    # Game loop
    while True:

        # Print contents of board
        print()
        print("board:")
        print("   0 1 2 3 4")
        for i in range(5):
            print(i,end="  ")
            for j in game.board[i]:
                print(j if j is not None else '-',end=" ")
            print()
        print()

        # Compute available actions
        available_actions = five_tigers.available_actions(game.board)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                row = int(input("Choose Row: "))
                column = int(input("Choose Column: "))
                if (row, column) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            copy_state = copy.deepcopy(game.board)
            state = board_to_state(game.player, copy_state)
            row, column = ai.choose_action(state, epsilon=False)
            print(f"AI chose to move row {row}, column {column}.")

        # Make move
        game.move((row, column))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            if game.winner == human_player:
                print(f"Winner is human")
            elif game.winner == 1-human_player:
                print(f"Winner is AI")
            else:
                print("Tie")
            print('scores:')
            print(f"Human: {game.scores[human_player]}")
            print(f"AI   : {game.scores[1-human_player]}")
            print("board:")
            print("   0 1 2 3 4")
            for i in range(5):
                print(i,end="  ")
                for j in game.board[i]:
                    print(j if j is not None else '-',end=" ")
                print()
            print()
            return
