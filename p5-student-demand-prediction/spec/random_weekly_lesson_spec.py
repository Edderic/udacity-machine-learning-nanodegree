import sys, os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from specter import Spec, expect
from weekly_lessons import RandomWeeklyLesson
from weekly_lessons import WeeklyLesson
from timezone import Timezone
import math

def should_be_in_range(item, rng=None):
    return (item >= rng['min']) & (item <= rng['max'])

def should_have_legitimate_minute_start_time(start_time):
    minutes = math.ceil(start_time) - start_time
    return (minutes == 0.0 or minutes == 0.25 or minutes == 0.5 or minutes == 0.75)

def should_be_in_standard_tz_format(tz_string):
    mapping = Timezone.mapping()
    standard_timezones = mapping.values()
    return tz_string in standard_timezones

class WeeklyLessonSpec(Spec):
    class timezone(Spec):
        def should_return_it(self):
            tz = Timezone('Abu Dhabi')
            wl = WeeklyLesson(start_time=5, day_of_week=0, timezone=tz)
            expect(wl.timezone()).to.equal(tz)

    class start_time(Spec):
        def should_return_it(self):
            wl = WeeklyLesson(start_time=5, day_of_week=0, timezone=Timezone('Abu Dhabi'))
            expect(wl.start_time()).to.equal(5)

    class day_of_week(Spec):
        def should_return_it(self):
            wl = WeeklyLesson(start_time=5, day_of_week=0, timezone=Timezone('Abu Dhabi'))
            expect(wl.day_of_week()).to.equal(0)

class RandomWeeklyLessonSpec(Spec):
    class by_default(Spec):
        def should_generate_random_day_of_week(self):
            rwl = RandomWeeklyLesson()
            rng = {'min': 0, 'max': 6}
            expect(should_be_in_range(rwl.day_of_week(), rng=rng)).to.be_true()

        def should_generate_random_start_time_should_be_in_right_range(self):
            rwl = RandomWeeklyLesson()
            rng = {'min': 0, 'max': 23.75}

            expect(should_be_in_range(rwl.start_time(), rng=rng)).to.be_true()

        def should_generate_random_start_time_in_fifteen_minute_increments(self):
            rwl = RandomWeeklyLesson()

            expect(should_have_legitimate_minute_start_time(rwl.start_time())).to.be_true()

        def should_generate_random_tz(self):
            tz = Timezone()
            rwl = RandomWeeklyLesson(timezone=tz)
            expect(rwl.timezone()).to.equal(tz)

    class adding_day_range(Spec):
        def should_respect_the_day_range(self):
            rwl = RandomWeeklyLesson(day_of_week_range=(0,4))
            rng = {'min': 0, 'max': 4}
            expect(should_be_in_range(rwl.day_of_week(), rng=rng)).to.equal(True)

    class adding_start_time_range(Spec):
        def should_respect_the_start_time_range(self):
            rwl = RandomWeeklyLesson(start_time_range=(8,20))
            rng = {'min': 8, 'max': 20}

            expect(should_be_in_range(rwl.start_time(), rng=rng)).to.equal(True)

