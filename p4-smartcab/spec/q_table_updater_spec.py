import json
from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'smartcab'))
import q_table_updater
import q_table

class Qtable_updater(Spec):
    class update(Spec):
        def should_take_into_account_alpha_gamma_and_max_q_values(self):
            light = 'red'
            next_waypoint = 'forward'
            left = None
            oncoming = None
            action = None
            reward = 1.0

            table = q_table.QTable(alpha=0.123,gamma=0.567)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=None,
                    new_value=0.0)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='forward',
                    new_value=0.340)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='left',
                    new_value=0.440)

            table.set_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action='right',
                    new_value=0.540)

            updater = q_table_updater.QTableUpdater(table)

            updater.update(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=action,
                    reward=reward)

            new_value = table.get_value_at(light=light,
                    next_waypoint=next_waypoint,
                    left=left,
                    oncoming=oncoming,
                    action=action)

            # new_value = old_value * (1 - self._alpha) + self._alpha * (reward + self._gamma * max_q)
            # 0.0 * (1 - 0.123) +  0.123 * (1.0 + 0.567 * 0.540)

            expect(round(new_value, 5)).to.equal(round(0.16066014, 5))
