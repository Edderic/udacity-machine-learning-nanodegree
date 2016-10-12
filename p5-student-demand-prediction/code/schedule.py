import numpy as np
import pandas as pd
from weekly_lessons import WeeklyLesson
from timezone import Timezone
from bins import Bins

# TODO: make sure that ActualSchedule implements methods of Schedule?
class ActualSchedule():
    def __init__(self, data_df):
        self._data_df = data_df
        self._schedule = Schedule()


        for i in data_df.index.values:
            row = data_df.ix[i]
            lessons = []
            for j in range(1, int(row.schedule_type + 1)):
                lessons.append(WeeklyLesson(start_time=row['l{}_time'.format(j)],
                    day_of_week=row['l{}_day'.format(j)]))

            new_value = self._schedule.add_schedule(Schedule(lessons=lessons,
                timezone=Timezone(row['user_tz'])))

            self._schedule = new_value

    def bins(self):
        return Bins(schedule=self._schedule).bins()

class Schedule():
    NUM_DAYS = 7
    NUM_START_TIMES = 96
    QUARTERS_IN_AN_HOUR = 4


    def __init__(self, lessons=[], timezone=None, table_df=pd.DataFrame()):
        self._timezone = timezone

        if table_df.empty:
            self._table_df = pd.DataFrame(np.zeros((Schedule.NUM_START_TIMES, Schedule.NUM_DAYS)))
        else:
            self._table_df = table_df

        for lesson in lessons:
            self.add_lesson(lesson)

    def __getitem__(self, index):
        return self._table_df[index]

    def ix(self, start_index, end_index):
        return self._table_df.ix[start_index:end_index]

    def sum(self):
        return self._table_df.sum()

    def timezone(self):
        return self._timezone

    def add_schedule(self, other_schedule, timezone=None):
        new_table = self._table_df.values + other_schedule._table_df.values

        return Schedule(table_df=pd.DataFrame(new_table), timezone=timezone)

    def freq_lessons_at(self, start_time=None, day_of_week=None):
        return self._table_df[day_of_week][self.convert_start_time_to_index(start_time)]

    def add_lesson(self, lesson):
        start_time = lesson.start_time()
        day_of_week = lesson.day_of_week()

        val = self._table_df[day_of_week][int(self.convert_start_time_to_index(start_time))]
        self._table_df.set_value(index=self.convert_start_time_to_index(start_time),
                col=day_of_week, value=val+1)

    def convert_start_time_to_index(self, start_time):
        return int(start_time * self.QUARTERS_IN_AN_HOUR)

