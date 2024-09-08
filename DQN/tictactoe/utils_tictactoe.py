import base64
import random
from itertools import zip_longest

import imageio
import IPython
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import tensorflow as tf
from statsmodels.iolib.table import SimpleTable


SEED = 0              # seed for pseudo-random number generator
MINIBATCH_SIZE = 64   # mini-batch size
TAU = 1e-3            # soft update parameter
E_DECAY = 0.999       # ε decay rate for ε-greedy policy
E_MIN = 0.05          # minimum ε value for ε-greedy policy
BOARD_SIZE = 3
ALL_ACTIONS = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]

random.seed(SEED)

# get suitable input for nn with batch_size = MINIBATCH_SIZE = 64
def get_experiences(memory_buffer):
    experiences = random.sample(memory_buffer, k=MINIBATCH_SIZE) #list
    states = tf.convert_to_tensor(np.array([np.array(e.state).flatten() for e in experiences if e is not None]),dtype=tf.float32) # (64,9) tensor
    actions = tf.convert_to_tensor(np.array([ALL_ACTIONS.index(e.action) for e in experiences if e is not None]), dtype=tf.int32) # (64,) tensor
    rewards = tf.convert_to_tensor(np.array([e.reward for e in experiences if e is not None]), dtype=tf.float32) # (64,) tensor
    next_states = tf.convert_to_tensor(np.array([np.array(e.next_state).flatten() for e in experiences if e is not None]),dtype=tf.float32) # (64,9) tensor
    done_vals = tf.convert_to_tensor(np.array([e.done for e in experiences if e is not None]).astype(np.uint8),           # (64,) tensor
                                     dtype=tf.float32)
    return (states, actions, rewards, next_states, done_vals)


def check_update_conditions(t, num_steps_upd, memory_buffer):
    if t % num_steps_upd == 2 and len(memory_buffer) > MINIBATCH_SIZE:
        return True
    else:
        return False
    
    
def get_new_eps(epsilon):
    return max(E_MIN, E_DECAY*epsilon)

# get available and best/random actions
def get_action(q_values, state, epsilon=0):
    state = tf.squeeze(state).numpy()  # (9,)
    valid_actions = [i for i in range(9) if state[i] == 0]  # 0 is available
    # make best action
    if random.random() > epsilon:
        # add -100 to inavailable actions to avoid making repetitive move
        action_mask = tf.convert_to_tensor(np.array([0 if i in valid_actions else -100 for i in range(9)]),dtype=tf.float32)
        q_values = q_values[0] + action_mask
        return ALL_ACTIONS[tf.argmax(q_values).numpy()]
    # make random action
    else:
        return ALL_ACTIONS[random.choice(valid_actions)]
    
# use soft update to update target q network
def update_target_network(q_network, target_q_network):
    for target_weights, q_net_weights in zip(target_q_network.weights, q_network.weights):
        target_weights.assign(TAU * q_net_weights + (1.0 - TAU) * target_weights)
    

def plot_history(reward_history, rolling_window=20, lower_limit=None,
                 upper_limit=None, plot_rw=True, plot_rm=True):
    
    if lower_limit is None or upper_limit is None:
        rh = reward_history
        xs = [x for x in range(len(reward_history))]
    else:
        rh = reward_history[lower_limit:upper_limit]
        xs = [x for x in range(lower_limit,upper_limit)]
    
    df = pd.DataFrame(rh)
    rollingMean = df.rolling(rolling_window).mean()

    plt.figure(figsize=(10,7), facecolor='white')
    
    if plot_rw:
        plt.plot(xs, rh, linewidth=1, color='cyan')
    if plot_rm:
        plt.plot(xs, rollingMean, linewidth=2, color='magenta')

    text_color = 'black'
        
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.grid()
#     plt.title("Total Point History", color=text_color, fontsize=40)
    plt.xlabel('Episode', color=text_color, fontsize=30)
    plt.ylabel('Total Points', color=text_color, fontsize=30)
    yNumFmt = mticker.StrMethodFormatter('{x:,}')
    ax.yaxis.set_major_formatter(yNumFmt)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    plt.show()
    
    