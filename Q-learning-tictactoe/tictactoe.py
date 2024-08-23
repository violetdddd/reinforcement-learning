import math
import random
import time
import numpy as np
import copy

X = "X"
O = "O"
EMPTY = None

class Tictactoe():

    def __init__(self, initial=[[EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY],
                                [EMPTY, EMPTY, EMPTY]]):
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
        self.left = 9

    @classmethod
    def available_actions(cls, board):
        """
        Tictactoe.available_actions(board) takes a `board` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of make a move in raw_i,column_j
        """
        actions = set()
        for i in range(3) :
            for j in range(3) :
                if board[i][j] == EMPTY :
                    actions.add((i,j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Tictactoe.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Tictactoe.other_player(self.player)

    def now_player_sign(self):
        if self.player == 0:
            return X
        else:
            return O
        
    #def update_score(self):
    #    def add_score(base_sign,score):
    #        if base_sign == X:
    #                self.scores[0] += score
    #        else:
    #                self.scores[1] += score
    #    def check_raw():
    #        for i in range(5):
    #            base_sign = self.board[i][0]
    #            if base_sign is not None and self.board[i][1] == base_sign and self.board[i][2] == base_sign and self.board[i][3] == base_sign and self.board[i][4] == base_sign:
    #                add_score(base_sign,5)
    #    def check_column():
    #        for i in range(5):
    #            base_sign = self.board[0][i]
    #            if base_sign is not None and self.board[1][i] == base_sign and self.board[2][i] == base_sign and self.board[3][i] == base_sign and self.board[4][i] == base_sign:
    #                add_score(base_sign,5)
    #    def check_5x():
    #        base_sign = self.board[2][2]
    #        if base_sign is not None and self.board[0][0] == base_sign and self.board[1][1] == base_sign and self.board[3][3] == base_sign and self.board[4][4] == base_sign:
    #            add_score(base_sign,5)
    #        if base_sign is not None and self.board[0][4] == base_sign and self.board[1][3] == base_sign and self.board[3][1] == base_sign and self.board[4][0] == base_sign:
    #            add_score(base_sign,5)
    #    def check_4x():
    #        base_sign = self.board[0][3]
    #        if base_sign is not None and self.board[1][2] == base_sign and self.board[2][1] == base_sign and self.board[3][0] == base_sign:
    #            add_score(base_sign,4)
    #        base_sign = self.board[0][1]
    #        if base_sign is not None and self.board[1][2] == base_sign and self.board[2][3] == base_sign and self.board[3][4] == base_sign:
    #            add_score(base_sign,4)
    #        base_sign = self.board[4][3]
    #        if base_sign is not None and self.board[3][2] == base_sign and self.board[2][1] == base_sign and self.board[1][0] == base_sign:
    #            add_score(base_sign,4)
    #        base_sign = self.board[4][1]
    #        if base_sign is not None and self.board[3][2] == base_sign and self.board[2][3] == base_sign and self.board[1][4] == base_sign:
    #            add_score(base_sign,4)
    #    def check_3x():
    #        base_sign = self.board[0][2]
    #        if base_sign is not None and self.board[1][1] == base_sign and self.board[2][0] == base_sign:
    #            add_score(base_sign,3)
    #        base_sign = self.board[0][2]
    #        if base_sign is not None and self.board[1][3] == base_sign and self.board[2][4] == base_sign:
    #            add_score(base_sign,3)
    #        base_sign = self.board[4][2]
    #        if base_sign is not None and self.board[3][1] == base_sign and self.board[2][0] == base_sign:
    #            add_score(base_sign,3)
    #        base_sign = self.board[4][2]
    #        if base_sign is not None and self.board[3][3] == base_sign and self.board[2][4] == base_sign:
    #            add_score(base_sign,3)
    #    def check_big5():
    #        base_sign = self.board[2][2]
    #        if base_sign is not None and self.board[0][0] == base_sign and self.board[4][0] == base_sign and self.board[0][4] == base_sign and self.board[4][4] == base_sign:
    #            add_score(base_sign,10)
    #    def check_small5():
    #        for i in range(1,4):
    #            for j in range(1,4):
    #                base_sign = self.board[i][j]
    #                if base_sign is not None and self.board[i-1][j-1] == base_sign and self.board[i-1][j+1] == base_sign and self.board[i+1][j-1] == base_sign and self.board[i+1][j+1] == base_sign:
    #                    add_score(base_sign,5)
    #    def check_well():
    #        for i in range(4):
    #            for j in range(4):
    #                base_sign = self.board[i][j]
    #                if base_sign is not None and self.board[i][j+1] == base_sign and self.board[i+1][j] == base_sign and self.board[i+1][j+1] == base_sign:
    #                    add_score(base_sign,1)
    #    self.scores = [0,0]
    #    check_3x()
    #    check_4x()
    #    check_5x()
    #    check_big5()
    #    check_column()
    #    check_raw()
    #    check_small5()
    #    check_well()

    def check_winner(self):
        for i in range(3):
            base_sign=self.board[i][1]
            if base_sign != EMPTY and self.board[i][0] == base_sign and base_sign == self.board[i][2]:
                if base_sign == X :
                    return 0
                else:
                    return 1
        for i in range(3):
            base_sign=self.board[1][i]
            if base_sign != EMPTY and self.board[0][i] == base_sign and base_sign == self.board[2][i]:
                if base_sign == X :
                    return 0
                else:
                    return 1
        base_sign=self.board[1][1]
        if base_sign != EMPTY:
            if self.board[0][0] == base_sign and self.board[2][2] == base_sign :
                if base_sign == X :
                    return 0
                else:
                    return 1
            elif self.board[0][2] == base_sign and self.board[2][0] == base_sign :
                if base_sign == X :
                    return 0
                else:
                    return 1
        return None
        
    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        raw, column = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif raw < 0 or raw >= 3 or column < 0 or column >= 3:
            raise Exception("Invalid move")

        # Update board
        self.board[raw][column] = self.now_player_sign()
        self.switch_player()
        self.left -= 1

        # Check for a winner
        self.winner = self.check_winner()
            


class TictactoeAI():

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
        for i in range(3) :
            for j in range(3) :
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
        for i in range(3) :
            for j in range(3) :
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

    player = TictactoeAI()

    def board_to_state(player,copy_state):
        translation = {X:1-player, O:player}
        state = [tuple([translation[j] if j in translation else j for j in copy_state[i]]) for i in range(3)]
        return state
    
    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Tictactoe()
        if 10000 < i < 20000:
            player.epsilon = 0.5
        elif 20000 < i < 30000:
            player.epsilon = 0.3
        elif i > 30000:
            player.epsilon = 0.1
        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None},
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


            # Make move
            game.move(action)
            copy_new_state = copy.deepcopy(game.board)
            new_state = board_to_state(game.player, copy_new_state)

            # When game is over, update Q values with rewards
            if game.winner is not None:
                new_state_last = board_to_state(1-game.player, copy_new_state)
                if game.winner == game.player:
                    player.update(state, action, new_state_last, -10)
                    player.update(
                        last[game.player]["state"],
                        last[game.player]["action"],
                        new_state,
                        3
                    )
                if game.winner == 1-game.player:
                    player.update(state, action, new_state_last, 3)
                    player.update(
                        last[game.player]["state"],
                        last[game.player]["action"],
                        new_state,
                        -10
                    )
                break

            # If game is continuing, no rewards yet
            elif game.left == 0:
                new_state_last = board_to_state(1-game.player, copy_new_state)
                player.update(state, action, new_state_last, 0.01)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0.01
                )
                break
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
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
        state = [tuple([translation[j] if j in translation else j for j in copy_state[i]]) for i in range(3)]
        return state
    
    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Tictactoe()

    # Game loop
    while True:

        # Print contents of board
        print()
        print("board:")
        print("   0 1 2")
        for i in range(3):
            print(i,end="  ")
            for j in game.board[i]:
                print(j if j is not None else '-',end=" ")
            print()
        print()

        # Compute available actions
        available_actions = Tictactoe.available_actions(game.board)
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
        if game.winner is not None or game.left == 0:
            print()
            print("GAME OVER")
            if game.winner == human_player:
                print(f"Winner is human")
            elif game.winner == 1-human_player:
                print(f"Winner is AI")
            else:
                print("Tie")
            print("board:")
            print("   0 1 2")
            for i in range(3):
                print(i,end="  ")
                for j in game.board[i]:
                    print(j if j is not None else '-',end=" ")
                print()
            print()
            return
