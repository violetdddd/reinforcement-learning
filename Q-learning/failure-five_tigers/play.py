from five_tigers import five_tigersAI, play, train
import numpy as np


# Load
#read_q = np.load('ai.npy', allow_pickle=True).item()
#ai = five_tigersAI(read_q)





# Save
# actually training a million times and get 1G data for Q dict can not teach ai to win the game
ai = train(1000000)  
np.save('ai.npy',ai.q)

play(ai)
