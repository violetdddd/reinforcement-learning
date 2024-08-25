from five_tigers import five_tigersAI, play, train
import numpy as np


# Load
read_q = np.load('ai_q6.npy', allow_pickle=True).item()
ai = five_tigersAI(read_q)





# Save
#ai = train(1000000)
#np.save('ai_q6.npy',ai.q)

play(ai)
