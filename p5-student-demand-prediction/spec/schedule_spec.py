from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from weekly_lessons import WeeklyLesson
from schedule import Schedule
from schedule import ActualSchedule
from timezone import Timezone
import pandas as pd

class ActualScheduleSpec(Spec):
    class when_given_data_for_the_month(Spec):
        def converts_it_to_an_actual_schedule(self):
            user_tz = ["Brasilia",
                    "Brasilia",
                    "Pacific (US & Canada)",
                    "Eastern (US & Canada)",
                    "Brasilia"
                    ]

            l1_time = range(0, 5)
            l1_day = range(0, 5)
            l2_time = range(1, 6)
            l2_day = range(0, 5)
            l3_time = range(2, 7)
            l3_day = range(0, 5)
            l4_time = range(3, 8)
            l4_day = range(0, 5)

            schedule_type = [4,4,4,4,4]

            args = {
                    'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l1_day': l1_day,
                    'l2_time': l2_time,
                    'l2_day': l2_day,
                    'l3_time': l3_time,
                    'l3_day': l3_day,
                    'l4_time': l4_time,
                    'l4_day': l4_day,
                    'schedule_type': schedule_type
                    }

            unique_user_summaries = pd.DataFrame(args)
            schedule = ActualSchedule(unique_user_summaries)
            bins = schedule.bins()
            expect(bins[0]).to.equal(10)
            expect(bins[1]).to.equal(10)
            expect(bins[2]).to.equal(0)
            expect(bins[3]).to.equal(0)
            expect(bins[4]).to.equal(0)
            expect(bins[5]).to.equal(0)

class ScheduleSpec(Spec):
    class timezone(Spec):
        def should_return_the_timezone_object(self):
            timezone = Timezone('Abu Dhabi')
            l1_1 = WeeklyLesson(start_time=0, day_of_week=0)
            l1_2 = WeeklyLesson(start_time=1, day_of_week=0)
            l1_3 = WeeklyLesson(start_time=0.5, day_of_week=0)
            lessons = [l1_1, l1_2, l1_3]

            s = Schedule(lessons=lessons, timezone=timezone)

            expect(s.timezone()).to.equal(timezone)
    class add_schedule(Spec):
        class when_timezones_dont_matter(Spec):
            def should_add_schedules_directly(self):
                timezone_1 = Timezone('Abu Dhabi')
                timezone_2 = Timezone('Pacific (US & Canada)')

                l1_1 = WeeklyLesson(start_time=0, day_of_week=0)
                l1_2 = WeeklyLesson(start_time=1, day_of_week=0)
                l1_3 = WeeklyLesson(start_time=0.5, day_of_week=0)

                l2_1 = WeeklyLesson(start_time=0, day_of_week=0)
                l2_2 = WeeklyLesson(start_time=1, day_of_week=0)
                l2_3 = WeeklyLesson(start_time=0.5, day_of_week=0)

                lessons_1 = [l1_1, l1_2, l1_3]
                lessons_2 = [l2_1, l2_2, l2_3]

                s_1 = Schedule(lessons=lessons_1, timezone=timezone_1)
                s_2 = Schedule(lessons=lessons_2, timezone=timezone_2)

                s_3 = s_1.add_schedule(s_2, timezone=None)

                expect(s_3.freq_lessons_at(start_time=0, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=1, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=0.5, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=23.5, day_of_week=5)).to.equal(0)

    class sum(Spec):
        def should_delegate_to_df(self):

            l1_1 = WeeklyLesson(start_time=0, day_of_week=0)
            l1_2 = WeeklyLesson(start_time=1, day_of_week=0)
            l1_3 = WeeklyLesson(start_time=0.5, day_of_week=0)

            lessons_1 = [l1_1, l1_2, l1_3]

            s = Schedule(lessons=lessons_1, timezone=Timezone('Abu Dhabi'))
            expect(s.sum().sum()).to.equal(3)

