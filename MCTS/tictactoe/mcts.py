#
# MCTS algorithm implementation
#

# packages
import math
import random

iterations = 1000

# tree node class definition
class TreeNode():
    # class constructor (create tree node class instance)
    def __init__(self, board, parent): # board is a class(win,draw,player,board,valid actions,move), parent is a node
        # init associated board state
        self.board = board
        
        # init is node terminal flag
        if self.board.is_win() or self.board.is_draw():
            # we have a terminal node
            self.is_terminal = True
        
        # otherwise
        else:
            # we have a non-terminal node
            self.is_terminal = False
        
        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal
        
        # init parent node if available
        self.parent = parent
        
        # init the number of node visits
        self.visits = 0
        
        # init the total score of the node
        self.score = 0
        
        # init current node's children
        self.children = {}

# MCTS class definition
class MCTS():
    # search for the best move in the current position
    def search(self, initial_state):
        # create root node
        self.root = TreeNode(initial_state, None)

        # walk through 1000 iterations
        for iteration in range(iterations):
            # select a node (selection phase)
            node = self.select(self.root)
            
            # scrore current node (simulation phase)
            score = self.rollout(node.board)
            
            # backpropagate results
            self.backpropagate(node, score)
        
        # pick up the best move in the current position
        try:
            return self.get_best_move(self.root, 0) # (i,j)tuple
        
        except:
            pass
    
    # select most promising node
    def select(self, node):
        # make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            # case where the node is fully expanded
            if node.is_fully_expanded:
                action = self.get_best_move(node, 2)
                node = node.children[action]
            
            # case where the node is not fully expanded 
            else:
                # otherwise expand the node
                return self.expand(node)
       
        # return node
        return node
    
    # expand node
    def expand(self, node):
        # generate legal actions for the given node
        actions = node.board.generate_actions() # a list containing (i,j) actions
        
        # loop over generated actions
        for action in actions:
            # make sure that current state (move) is not present in child nodes
            if action not in node.children:
                # create a new node
                state = node.board.move(action) # a Board class
                new_node = TreeNode(state, node)
                
                # add child node to parent's node children list (dict)
                node.children[action] = new_node
                
                # case when node is fully expanded
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                
                # return newly created node
                return new_node
        
        # debugging
        print('Should not get here!!!')
    
    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        current = board.player # who's turn to play next
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            # try to make a move
            try:
                # make the on board
                action = random.choice(board.generate_actions())
                board = board.move(action)
                
            # no moves available
            except:
                # return a draw score
                return 0
        
        # return score from the current player perspective
        if board.player == current: return 1
        elif board.player == -current: return -1
                
    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1
            
            # update node's score
            node.score += score
            score = -score

            # set node to parent
            node = node.parent
    
    # select the best node basing on UCB1 formula
    def get_best_move(self, node, exploration_constant):
        # define best score & best moves
        best_score = float('-inf')
        best_moves = []
        
        # loop over child nodes
        for action, child_node in node.children.items():
            
            # get move score using UCT formula
            move_score = child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))                                        

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [action]
            
            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(action)
            
        # return one of the best moves randomly
        return random.choice(best_moves)



























