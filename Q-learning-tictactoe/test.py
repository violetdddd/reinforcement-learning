import numpy as np
read_q = np.load('ai_q7.npy', allow_pickle=True).item()
print(read_q[(((1, None, None), (0, 0, None), (1, None, None)), (0, 2))],
      read_q[(((1, None, None), (0, 0, None), (1, None, None)), (1, 2))],
      read_q[(((1, None, None), (0, 0, None), (1, None, None)), (2, 2))])