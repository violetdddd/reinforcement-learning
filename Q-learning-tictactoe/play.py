from tictactoe import TictactoeAI, play
import numpy as np
import pickle


# Load
read_q = np.load('ai_q10.npy', allow_pickle=True).item()


ai = TictactoeAI(read_q)

play(ai, 1)
