import random
import pandas
import numpy
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from q_table import QTable

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.q_table = QTable(alpha=0.1, gamma=0.1)
        self.total_actions = 0.0
        self.total_rewards = 0.0
        # self.last_occurence_of_punishment = 0.0

    def set_q_table(self, alpha=0.0, gamma=0.0):
        self.q_table = QTable(alpha=alpha, gamma=gamma)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator

        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        self.state = 'light: {}, left: {}, oncoming: {}, next_waypoint: {}'.format(inputs['light'],
                inputs['left'],
                inputs['oncoming'],
                self.next_waypoint)

        # Select action according to your policy
        action = self.q_table.best_action(light=inputs['light'],
                next_waypoint=self.next_waypoint,
                left=inputs['left'],
                oncoming=inputs['oncoming'])

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Learn policy based on state, action, reward
        self.q_table.update(light=inputs['light'],
                next_waypoint=self.next_waypoint,
                left=inputs['left'],
                oncoming=inputs['oncoming'],
                action=action,
                reward=reward)

        self.total_rewards += reward
        self.total_actions += 1.0

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, next_waypoint = {}".format(deadline, inputs, action, reward, self.next_waypoint)  # [debug]

    def __init_q_table(self):
        self.q_table = {}

    def __positions(self):
        positions_list = []
        for i in range(6):
            for j in range(8):
                positions_list.append((i+1,j+1))
        return positions_list

def simulate(alpha=0.0, gamma=0.0):
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track
    a.set_q_table(alpha=alpha, gamma=gamma)

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit

def experiment_with_different_alpha_gamma_values():
    alpha_values = [0.1, 0.3, 0.7, 0.9]
    gamma_values = [0.1, 0.3, 0.7, 0.9]

    alphas = []
    gammas = []
    avg_total_actions = []
    avg_total_rewards = []
    std_total_actions = []
    std_total_rewards = []
    # last_occurrence_of_punishments = []

    for alpha in alpha_values:
        for gamma in gamma_values:
            avg_total_actions_in_experiments = []
            avg_total_rewards_in_experiments = []
            std_total_actions_in_experiments = []
            std_total_rewards_in_experiments = []

            for experiment in range(10):
                a = simulate(alpha=alpha, gamma=gamma)

                avg_total_actions_in_experiments.append(a.total_actions)
                avg_total_rewards_in_experiments.append(a.total_rewards)

            alphas.append(alpha)
            gammas.append(gamma)

            avg_total_actions.append(numpy.average(avg_total_actions_in_experiments))
            avg_total_rewards.append(numpy.average(avg_total_rewards_in_experiments))
            std_total_actions.append(numpy.std(avg_total_actions_in_experiments))
            std_total_rewards.append(numpy.std(avg_total_rewards_in_experiments))


    pandas.DataFrame({'alpha': alphas,
        'gamma': gammas,
        'avg_total_actions': avg_total_actions,
        'avg_total_rewards': avg_total_rewards,
        'std_total_actions': std_total_actions,
        'std_total_rewards': std_total_rewards
        }).to_csv('alpha_gamma_experiments.csv')



def run():
    """Run the agent for a finite number of trials."""

    experiment_with_different_alpha_and_gamma_values = False

    if experiment_with_different_alpha_and_gamma_values:
        experiment_with_different_alpha_gamma_values()
    else:
        simulate(alpha=0.9, gamma=0.3)

if __name__ == '__main__':
    run()
