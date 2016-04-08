class QTableUpdater():
    def __init__(self, table):
        self.table = table

    def update(self,
            light=None,
            oncoming=None,
            next_waypoint=None,
            action=None,
            left=None,
            reward=0.0):

        old_value = self.table.get_value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=action)

        new_value = old_value * (1 - self.table._alpha) + self.table._alpha * (reward + self.table._gamma * self.table.max_q(light=light, oncoming=oncoming, next_waypoint=next_waypoint, left=left))

        self.table.set_value_at(light=light,
                next_waypoint=next_waypoint,
                left=left,
                oncoming=oncoming,
                action=action,
                new_value=new_value)
