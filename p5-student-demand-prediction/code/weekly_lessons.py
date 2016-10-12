import numpy as np
import pandas as pd
from timezone import Timezone

class RandomWeeklyLesson():
    START_TIME_TO_INDEX_MULTIPLIER = 4

    def __init__(self,
            day_of_week_range=(0, 7,),
            start_time_range=(0, 23.75,),
            timezone=None):
        dw_low, dw_high = day_of_week_range
        self._day_of_week = np.random.randint(low=dw_low,
                high=dw_high) # [0,6]; seven days in a week
        self._start_time = self.generate_start_time(start_time_range) # [0, 23.75]
        self._timezone = timezone or np.random.choice(Timezone.mapping().values())

    def day_of_week(self):
        return self._day_of_week

    def start_time(self):
        return self._start_time

    def timezone(self):
        return self._timezone

    # helper
    def generate_start_time(self, start_time_range):
        st_min, st_max = start_time_range
        sti_min = self.convert_to_start_time_index(st_min)
        sti_max = self.convert_to_start_time_index(st_max)

        return np.random.randint(sti_min, sti_max) / RandomWeeklyLesson.START_TIME_TO_INDEX_MULTIPLIER

    def convert_to_start_time_index(self, start_time):
        return start_time * RandomWeeklyLesson.START_TIME_TO_INDEX_MULTIPLIER

    def discretize_start_time(self,start_time):
        integer = int(start_time)
        decimals = start_time - integer

        df = pd.DataFrame({'discrete_decimal_values': [0.0, 0.25, 0.50, 0.75],
            'actual_decimal_values': np.ones(4) * decimals
            })

        closest_index = (df.discrete_decimal_values - df.actual_decimal_values).abs().argmin()

        st = integer + df.ix[closest_index].discrete_decimal_values
        return st


class WeeklyLesson():
    def __init__(self, day_of_week=None, start_time=None, timezone=None):
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._timezone = timezone

    def day_of_week(self):
        return self._day_of_week

    def start_time(self):
        return self._start_time

    def timezone(self):
        return self._timezone

