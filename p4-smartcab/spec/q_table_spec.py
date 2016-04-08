import json
from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'smartcab'))
import q_table

class Qtable(Spec):
    class gamma(Spec):
        def should_return_the_gamma_value(self):
            alpha = 0.12121
            gamma = 0.45454
            table = q_table.QTable(alpha=alpha, gamma=gamma)
            expect(table.gamma()).to.equal(gamma)

    class alpha(Spec):
        def should_return_the_alpha_value(self):
            alpha = 0.12121
            gamma = 0.45454
            table = q_table.QTable(alpha=alpha, gamma=gamma)
            expect(table.alpha()).to.equal(alpha)

    class set_value_at(Spec):
        def should_set_the_value(self):
            alpha = 0.123
            gamma = 0.456
            light = 'red'
            next_waypoint = 'forward'
            left = None
            oncoming = None
            action = None

            table = q_table.QTable(alpha=alpha, gamma=gamma)
            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=action,
                    new_value=0.540)

            value = table.get_value_at(light=light,
                    left=left,
                    oncoming=oncoming,
                    next_waypoint=next_waypoint,
                    action=action)

            expect(value).to.equal(0.540)

    class get_value_at(Spec):
        def should_return_the_value_assigned(self):
            alpha = 0.123
            gamma = 0.456
            light = 'red'
            next_waypoint = 'forward'
            left = None
            oncoming = None
            action = None

            table = q_table.QTable(alpha=alpha, gamma=gamma)
            table._table["{}-{}-{}-{}-{}".format(str(light),
                str(left),
                str(oncoming),
                str(next_waypoint),
                str(action))] = 0.543

            value = table.get_value_at(light=light,
                    left=left,
                    oncoming=oncoming,
                    next_waypoint=next_waypoint,
                    action=action)

            expect(value).to.equal(0.543)
    class max_q(Spec):
        def should_return_the_highest_q_value_associated_with_states(self):
            alpha = 0.123
            gamma = 0.456
            light = 'red'
            next_waypoint = 'forward'
            left = None
            oncoming = None
            action = 'forward'

            table = q_table.QTable(alpha=alpha, gamma=gamma)
            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=action,
                    new_value=0.540)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='right',
                    new_value=0.440)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='left',
                    new_value=0.340)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=None,
                    new_value=0.240)

            max_q = table.max_q(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming)

            expect(max_q).to.equal(0.540)

    class best_action(Spec):
        def should_return_the_action_with_the_highest_q_value(self):
            alpha = 0.123
            gamma = 0.456
            light = 'red'
            next_waypoint = 'forward'
            left = None
            oncoming = None
            action = 'forward'

            table = q_table.QTable(alpha=alpha, gamma=gamma)
            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=action,
                    new_value=0.540)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='right',
                    new_value=0.440)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='left',
                    new_value=0.340)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=None,
                    new_value=0.240)

            best_action = table.best_action(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming)

            expect(best_action).to.equal('forward')
