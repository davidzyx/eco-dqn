import os
import pickle

import matplotlib.pyplot as plt
import numpy as np

import src.envs.core as ising_env
from experiments.utils import load_graph_set, mk_dir
from src.agents.dqn.dqn import DQN
from src.agents.dqn.utils import TestMetric
from src.envs.utils import (SetGraphGenerator,
                            RandomErdosRenyiGraphGenerator,
                            EdgeType, RewardSignal, ExtraAction,
                            OptimisationTarget, SpinBasis,
                            Observable,
                            DEFAULT_OBSERVABLES)
from src.networks.mpnn import MPNN

try:
    import seaborn as sns
    plt.style.use('seaborn')
except ImportError:
    pass

import time


def run_subsets():
    PERTUBED_OBSERVABLES_SETS = [
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        ### ------------------------ 6 choose 2 ------------------------ ###
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        ### ------------------------ 6 choose 1 ------------------------ ###
        [
            Observable.SPIN_STATE,                          #1
            Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            Observable.TERMINATION_IMMANENCY                #7
        ],
        ### ------------------------ only 1 ------------------------ ###
        [
            Observable.SPIN_STATE,                          #1
            # Observable.IMMEDIATE_REWARD_AVAILABLE,          #2
            # Observable.TIME_SINCE_FLIP,                     #3
            # Observable.DISTANCE_FROM_BEST_SCORE,            #4
            # Observable.DISTANCE_FROM_BEST_STATE,            #5
            # Observable.NUMBER_OF_GREEDY_ACTIONS_AVAILABLE,  #6
            # Observable.TERMINATION_IMMANENCY                #7
        ],
    ]

    for i, pertubed_set in enumerate(PERTUBED_OBSERVABLES_SETS):
        save_loc = f"ER_40spin_p{str(i).zfill(2)}/eco"
        if os.path.exists(save_loc):
            continue
        # print(save_loc)
        run(save_loc=save_loc)


def run(save_loc="ER_40spin/eco"):

    print("\n----- Running {} -----\n".format(os.path.basename(__file__)))

    ####################################################
    # SET UP ENVIRONMENTAL AND VARIABLES
    ####################################################

    gamma=0.95
    step_fact = 2

    env_args = {'observables':DEFAULT_OBSERVABLES,
                'reward_signal':RewardSignal.BLS,
                'extra_action':ExtraAction.NONE,
                'optimisation_target':OptimisationTarget.CUT,
                'spin_basis':SpinBasis.BINARY,
                'norm_rewards':True,
                'memory_length':None,
                'horizon_length':None,
                'stag_punishment':None,
                'basin_reward':1./40,
                'reversible_spins':True}

    ####################################################
    # SET UP TRAINING AND TEST GRAPHS
    ####################################################

    n_spins_train = 40

    train_graph_generator = RandomErdosRenyiGraphGenerator(n_spins=n_spins_train,p_connection=0.15,edge_type=EdgeType.DISCRETE)

    ####
    # Pre-generated test graphs
    ####
    graph_save_loc = "_graphs/testing/ER_40spin_p15_50graphs.pkl"
    graphs_test = load_graph_set(graph_save_loc)
    n_tests = len(graphs_test)

    test_graph_generator = SetGraphGenerator(graphs_test, ordered=True)

    ####################################################
    # SET UP TRAINING AND TEST ENVIRONMENTS
    ####################################################

    train_envs = [ising_env.make("SpinSystem",
                                 train_graph_generator,
                                 int(n_spins_train*step_fact),
                                 **env_args)]


    n_spins_test = train_graph_generator.get().shape[0]
    test_envs = [ising_env.make("SpinSystem",
                                test_graph_generator,
                                int(n_spins_test*step_fact),
                                **env_args)]

    ####################################################
    # SET UP FOLDERS FOR SAVING DATA
    ####################################################

    data_folder = os.path.join(save_loc,'data')
    network_folder = os.path.join(save_loc, 'network')

    mk_dir(data_folder)
    mk_dir(network_folder)
    # print(data_folder)
    network_save_path = os.path.join(network_folder,'network.pth')
    test_save_path = os.path.join(network_folder,'test_scores.pkl')
    loss_save_path = os.path.join(network_folder, 'losses.pkl')

    ####################################################
    # SET UP AGENT
    ####################################################

    nb_steps = 1200000  # 2500000

    network_fn = lambda: MPNN(n_obs_in=train_envs[0].observation_space.shape[1],
                              n_layers=3,
                              n_features=64,
                              n_hid_readout=[],
                              tied_weights=False)

    agent = DQN(train_envs,

                network_fn,

                init_network_params=None,
                init_weight_std=0.01,

                double_dqn=True,
                clip_Q_targets=False,

                replay_start_size=500,
                replay_buffer_size=5000,  # 20000
                gamma=gamma,  # 1
                update_target_frequency=1000,  # 500

                update_learning_rate=False,
                initial_learning_rate=1e-4,
                peak_learning_rate=1e-4,
                peak_learning_rate_step=20000,
                final_learning_rate=1e-4,
                final_learning_rate_step=200000,

                update_frequency=32,  # 1
                minibatch_size=64,  # 128
                max_grad_norm=None,
                weight_decay=0,

                update_exploration=True,
                initial_exploration_rate=1,
                final_exploration_rate=0.05,  # 0.05
                final_exploration_step=150000,  # 40000

                adam_epsilon=1e-8,
                logging=False,
                loss="mse",

                save_network_frequency=100000,
                network_save_path=network_save_path,

                evaluate=True,
                test_envs=test_envs,
                test_episodes=n_tests,
                test_frequency=10000,  # 10000
                test_save_path=test_save_path,
                test_metric=TestMetric.MAX_CUT,

                seed=None
                )

    print("\n Created DQN agent with network:\n\n", agent.network)

    #############
    # TRAIN AGENT
    #############
    start = time.time()
    agent.learn(timesteps=nb_steps, verbose=True)
    print(time.time() - start)

    agent.save()

    ############
    # PLOT - learning curve
    ############
    data = pickle.load(open(test_save_path,'rb'))
    data = np.array(data)

    fig_fname = os.path.join(network_folder,"training_curve")

    plt.plot(data[:,0],data[:,1])
    plt.xlabel("Training run")
    plt.ylabel("Mean reward")
    if agent.test_metric==TestMetric.ENERGY_ERROR:
      plt.ylabel("Energy Error")
    elif agent.test_metric==TestMetric.BEST_ENERGY:
      plt.ylabel("Best Energy")
    elif agent.test_metric==TestMetric.CUMULATIVE_REWARD:
      plt.ylabel("Cumulative Reward")
    elif agent.test_metric==TestMetric.MAX_CUT:
      plt.ylabel("Max Cut")
    elif agent.test_metric==TestMetric.FINAL_CUT:
      plt.ylabel("Final Cut")

    plt.savefig(fig_fname + ".png", bbox_inches='tight')
    plt.savefig(fig_fname + ".pdf", bbox_inches='tight')

    ############
    # PLOT - losses
    ############
    data = pickle.load(open(loss_save_path,'rb'))
    data = np.array(data)

    fig_fname = os.path.join(network_folder,"loss")

    N=50
    data_x = np.convolve(data[:,0], np.ones((N,))/N, mode='valid')
    data_y = np.convolve(data[:,1], np.ones((N,))/N, mode='valid')

    plt.plot(data_x,data_y)
    plt.xlabel("Timestep")
    plt.ylabel("Loss")

    plt.yscale("log")
    plt.grid(True)

    plt.savefig(fig_fname + ".png", bbox_inches='tight')
    plt.savefig(fig_fname + ".pdf", bbox_inches='tight')

    plt.clf()

if __name__ == "__main__":
    # run()
    run_subsets()