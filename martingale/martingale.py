""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
def author():  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    return "lzhang699"  # replace tb34 with your Georgia Tech username.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
def gtid():  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    return 903658227  # replace with your GT ID number  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		   	 		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    result = False  		  	   		   	 		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		   	 		  		  		    	 		 		   		 		  
        result = True  		  	   		   	 		  		  		    	 		 		   		 		  
    return result  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  

def betting_strategy(arr, win_prob=18 / (36 + 2), winning_target=80, bankroll=None):
    # total winnings
    episode_winnings = 0
    # num of black / num of black + num of red + two zeros
    arr[0] = 0
    spin_count = 0
    while episode_winnings < winning_target and spin_count < 1000 and (bankroll is None or episode_winnings > -bankroll):
        won = False
        bet_amount = 1
        while not won and spin_count < 1000:
            won = get_spin_result(win_prob)
            spin_count += 1
            if won == True:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount_double = bet_amount * 2
                bet_amount = bet_amount_double if bankroll is None or bet_amount_double < bankroll + \
                    episode_winnings else bankroll + episode_winnings
            arr[spin_count] = episode_winnings

    if episode_winnings == winning_target:
        for k in range(spin_count, 1001):
            arr[k] = winning_target

    if bankroll is not None and episode_winnings == -bankroll:
        for k in range(spin_count, 1001):
            arr[k] = -bankroll

    return arr

def test_code():  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # win_prob = 0.60  # set appropriately to the probability of a win  		  	   		   	 		  		  		    	 		 		   		 		  
    # np.random.seed(gtid())  # do this only once  		  	   		   	 		  		  		    	 		 		   		 		  
    # print(get_spin_result(win_prob))  # test the roulette spin  		  	   		   	 		  		  		    	 		 		   		 		  
    # # add your code here to implement the experiments  		  	   		   	 		  		  		    	 		 		   		 		  
    # betting_strategy(10)

    # Experiment 1 Figure 1
    episodes = 10
    outcomes = np.empty((episodes, 1001), int)
    for i in range(episodes):
        betting_strategy(outcomes[i])
        plt.plot(outcomes[i], label="Spin {}".format(i))

    plt.suptitle('Experiment1 Fig1: 10 Episodes')
    plt.xlabel("Successive Bets")
    plt.xlim([0, 300])
    plt.ylabel("Episode Winnings")
    plt.ylim([-256, 100])
    plt.legend()
    # plt.show()
    plt.savefig('experiment_1_figure_1.png')
    plt.close()

    # Experiment 1 Figure 2
    episodes = 1000
    outcomes = np.empty((episodes, 1001), int)
    for i in range(episodes):
        betting_strategy(outcomes[i])

    spins_mean = np.mean(outcomes, axis=0)
    spins_std = np.std(outcomes, axis=0)
    upper_band = spins_mean + spins_std
    lower_band = spins_mean - spins_std

    plt.suptitle('Experiment1 Fig2: 1000 Episodes - Mean & Standard Deviation')
    plt.plot(spins_mean, label='mean')
    plt.plot(upper_band, label='+std')
    plt.plot(lower_band, label='-std')
    plt.xlabel("Successive Bets")
    plt.xlim([0, 300])
    plt.ylabel("Episode Winnings Mean")
    plt.ylim([-256, 100])
    plt.legend()
    # plt.show()
    plt.savefig('experiment_1_figure_2.png')
    plt.close()

    # Experiment 1 Figure 3
    spins_median = np.median(outcomes, axis=0)
    spins_std = np.std(outcomes, axis=0)
    upper_band = spins_median + spins_std
    lower_band = spins_median - spins_std

    plt.suptitle('Experiment1 Fig3: 1000 Episodes - Median & Standard Deviation')
    plt.plot(spins_median, label='median')
    plt.plot(upper_band, label='+std')
    plt.plot(lower_band, label='-std')
    plt.xlabel("Successive Bets")
    plt.xlim([0, 300])
    plt.ylabel("Episode Winnings Median")
    plt.ylim([-256, 100])
    plt.legend()
    # plt.show()
    plt.savefig('experiment_1_figure_3.png')
    plt.close()

    # Just curious
    # episodes = 10
    # outcomes = np.empty((episodes, 1001), int)
    # for i in range(episodes):
    #     betting_strategy(outcomes[i], bankroll=256)
    #     plt.plot(outcomes[i])

    # plt.suptitle('Experiment1 Fig1: 10 Episodes with {} Bankroll'.format(256))
    # plt.xlabel("Successive Bets")
    # plt.xlim([0, 1000])
    # plt.ylabel("Episode Winnings")
    # plt.ylim([-256, 100])
    # # plt.legend()
    plt.show()

    # Experiment 2 Figure 1
    episodes = 1000
    bankroll = 256
    outcomes = np.empty((episodes, 1001), int)
    for i in range(episodes):
        betting_strategy(outcomes[i], bankroll=bankroll)

    spins_mean = np.mean(outcomes, axis=0)
    spins_std = np.std(outcomes, axis=0)
    upper_band = spins_mean + spins_std
    lower_band = spins_mean - spins_std

    plt.suptitle(
        'Experiment2 Fig1: 1000 Episodes with {} Bankroll - Mean & Standard Deviation'.format(bankroll))
    plt.plot(spins_mean, label='mean')
    plt.plot(upper_band, label='+std')
    plt.plot(lower_band, label='-std')
    plt.xlabel("Successive Bets")
    plt.xlim([0, 300])
    plt.ylabel("Episode Winnings Mean")
    plt.ylim([-256, 100])
    plt.legend()
    # plt.show()
    plt.savefig('experiment_2_figure_1.png')
    plt.close()

    # Experiment 2 Figure 2
    spins_median = np.median(outcomes, axis=0)
    spins_std = np.std(outcomes, axis=0)
    upper_band = spins_median + spins_std
    lower_band = spins_median - spins_std

    plt.suptitle(
        'Experiment2 Fig2: 1000 Episodes with {} Bankroll - Median & Standard Deviation'.format(bankroll))
    plt.plot(spins_median, label='median')
    plt.plot(upper_band, label='+std')
    plt.plot(lower_band, label='-std')
    plt.xlabel("Successive Bets")
    plt.xlim([0, 300])
    plt.ylabel("Episode Winnings Median")
    plt.ylim([-256, 100])
    plt.legend()
    # plt.show()
    plt.savefig('experiment_2_figure_2.png')
    plt.close()


if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    test_code()  		  	   		   	 		  		  		    	 		 		   		 		  
