# Udacity MLND P4: Train a Smartcab

## Tasks

### Setup

You need Python 2.7 and pygame for this project: https://www.pygame.org/wiki/GettingStarted
For help with installation, it is best to reach out to the pygame community [help page, Google group, reddit].

### Download

Download smartcab.zip, unzip and open the template Python file agent.py (do not modify any other file). Perform the following tasks to build your agent, referring to instructions mentioned in README.md as well as inline comments in agent.py.

Also create a project report (e.g. Word or Google doc), and start addressing the questions indicated in italics below. When you have finished the project, save/download the report as a PDF and turn it in with your code.

### Implement a basic driving agent

Implement the basic driving agent, which processes the following inputs at each time step:

Next waypoint location, relative to its current location and heading,
Intersection state (traffic light and presence of cars), and,
Current deadline value (time steps remaining),
And produces some random move/action (None, 'forward', 'left', 'right'). Don’t try to implement the correct strategy! That’s exactly what your agent is supposed to learn.

Run this agent within the simulation environment with enforce_deadline set to False (see run function in agent.py), and observe how it performs. In this mode, the agent is given unlimited time to reach the destination. The current state, action taken by your agent and reward/penalty earned are shown in the simulator.

#### In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?

The agent is randomly picking actions, no matter what the condition of
the environment. It does not care whether or not there is an oncoming
vehicle, nor does it care about vehicles on its left nor right. It also
seems to disregard the traffic light.

It seems to reward the following:

  Going right when traffic light is red:
    LearningAgent.update(): deadline = 20,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 2

    LearningAgent.update(): deadline = 14,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 2

    LearningAgent.update(): deadline = 13,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 2

    LearningAgent.update(): deadline = 12,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 0.5

    LearningAgent.update(): deadline = 11,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 2

    LearningAgent.update(): deadline = 8,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 0.5

  Going forward when traffic light is green:
    LearningAgent.update(): deadline = 19,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = forward,
     reward = 2

    LearningAgent.update(): deadline = 16,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = forward,
     reward = 0.5

  Going forward when traffic light is green and car in the right is trying to move forward:
    LearningAgent.update(): deadline = 10,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': 'forward',
     'left': None},
     action = forward,
     reward = 0.5

  Going right when traffic light is green:
    LearningAgent.update(): deadline = 11,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 2

    LearningAgent.update(): deadline = 6,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = right,
     reward = 0.5

  Staying at the same location when deadline is red:
    LearningAgent.update(): deadline = 17,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = None,
     reward = 1

  Staying at the same location when stoplight is green:
    LearningAgent.update(): deadline = 7,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = None,
     reward = 1

    LearningAgent.update(): deadline = 5,
     inputs = {'light': 'green',
     'oncoming': None,
     'right': None,
     'left': None},
     action = None,
     reward = 1

It penalizes the following:

  Going forward when the traffic light is red:
    LearningAgent.update(): deadline = 18,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = forward,
     reward = -1

    LearningAgent.update(): deadline = 15,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = forward,
     reward = -1

  Going left when the traffic light is red:
    LearningAgent.update(): deadline = 9,
     inputs = {'light': 'red',
     'oncoming': None,
     'right': None,
     'left': None},
     action = left,
     reward = -1

  Environment seems to prevent the car from moving forward, however...

It does eventually make it to the target location, but only through many
iterations, and it seems to take so long that it is way past the deadline.


Identify and update state

Identify a set of states that you think are appropriate for modeling the driving agent. The main source of state variables are current inputs, but not all of them may be worth representing. Also, you can choose to explicitly define states, or use some combination (vector) of inputs as an implicit state.

At each time step, process the inputs and update the current state. Run it again (and as often as you need) to observe how the reported state changes through the run.

Justify why you picked these set of states, and how they model the agent and its environment.
Report
------


## In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?


**
Justify why you picked these set of states, and how they model the agent and
its environment.

The states I picked are the following:

1. Coordinates of each location. This would let us know where our agent is
   on the map.
2. Stop light, whether it's green or red. We hope that the agent would learn
   to not go forward or left when it is red, but that it's okay to turn right on red.
3. Nearby vehicles and their direction. We hope that

`48 * 4 * 2 * 3 * 3 * 3 = 10368` states

Edge cases:

There is a car on the left wanting to go forward. It is red light. You want
to turn right.  The car on the left has the right of way.

Green Forward

Any nearby vehicles. If there are any cars on the left, right, or front, we
hope that our vehicle would learn to follow the U.S. rules on right of way.

To satisfy the constraint of having 100-iterations and net positive rewards
limit, we could do some state reduction.  We could try changing the rewards

To improve the model's performance, we could factor in the distance between
the location and the destination into the rewards.

To improve the model's performance, I could do some manual "feature reduction"
by writing all the edge cases into their own discrete state, or maybe, figu
