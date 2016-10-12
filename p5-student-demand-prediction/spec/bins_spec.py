from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))
from bins import Bins
from schedule import Schedule
from weekly_lessons import RandomWeeklyLesson

class BinsSpec(Spec):
    class when_given_a_schedule_and_num_bins(Spec):
        def it_should_aggregate_the_lesson_requests_per_bin(self):
            schedule = Schedule()
            schedule.add_lesson(RandomWeeklyLesson())

            b = Bins(schedule=schedule)
            expect(b.sum().sum()).to.equal(1)

    class num_bins(Spec):
        def by_default_should_be_6(self):
            schedule = Schedule()
            schedule.add_lesson(RandomWeeklyLesson())

            b = Bins(schedule=schedule)
            expect(b.num_bins()).to.equal(6)

    class check_bin_frequencies(Spec):
        def should_add_up(self):
            schedule = Schedule()
            schedule.add_lesson(RandomWeeklyLesson())
            schedule.add_lesson(RandomWeeklyLesson())

            b = Bins(schedule=schedule)
            b_ = b.bins()

            expect(b[0] + b[1] + b[2] + b[3] + b[4] + b[5]).to.equal(2)
            expect(b_[0] + b_[1] + b_[2] + b_[3] + b_[4] + b_[5]).to.equal(2)
