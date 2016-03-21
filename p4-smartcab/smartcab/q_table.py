# Given a state, figure out which action to take
    # best_action_given_state
# Take an action, get reward
# Update entry for old state-action

# TODO: refactor by extracting value object StateActionMapper
import json

class QTable():
    def __init__(self, alpha=1.00, gamma=0.5):
        self._alpha = alpha
        self._gamma = gamma
        self.__initialize_table()

    def alpha(self):
        return self._alpha

    def gamma(self):
        return self._gamma

    def __value_at(self, light=None, next_waypoint=None, left=None, oncoming=None, action=None):
        return self._table[self.__state_action(light=light,
            left=left,
            oncoming=oncoming,
            next_waypoint=next_waypoint,
            action=action)]

    def __set_value_at(self, light=None, next_waypoint=None, left=None, oncoming=None, action=None, new_value=0.0):
        self._table[self.__state_action(light=light,
            left=left,
            oncoming=oncoming,
            next_waypoint=next_waypoint,
            action=action)] = new_value

    def best_action(self, light=None, next_waypoint=None, left=None, oncoming=None):
        go_to_next_waypoint = self.__value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=next_waypoint)

        do_nothing = self.__value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=None)

        if go_to_next_waypoint >= do_nothing:
            return next_waypoint
        else:
            return None

    def update(self, light=None, next_waypoint=None, left=None, oncoming=None, action=None, reward=0.0):
        old_value = self.__value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=action)

        new_value = old_value * (1 - self._alpha) + self._alpha * (reward + self._gamma * old_value)

        self.__set_value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=action,
                new_value=new_value)

        # print "After update"
        # print json.dumps(self._table, indent=4)

        # import pdb; pdb.set_trace()

    def __next_waypoint(self, light, next_waypoint):
        return self._table['light'][light]['next_waypoint'][next_waypoint]

    def __state_action(self, light=None, left=None, oncoming=None, next_waypoint=None, action=None):
        return "{}-{}-{}-{}-{}".format(str(light), str(left), str(oncoming), str(next_waypoint), str(action))

    def __initialize_table(self):
        self._table = {}

        for light in ['red', 'green']:
            for left in ['forward', 'left', 'right', 'None']:
                for oncoming in ['forward', 'left', 'right', 'None']:
                    for next_waypoint in ['forward', 'left', 'right', 'None']:
                        for action in ['forward', 'left', 'right', 'None']:
                            self._table[self.__state_action(light=light,
                                left=left,
                                oncoming=oncoming,
                                next_waypoint=next_waypoint,
                                action=action)] = 0.0

