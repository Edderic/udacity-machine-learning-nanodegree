import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from specter import Spec, expect
from models import DumbModel
from backtest import BackTest
from dateutil.parser import parse

class BackTestSpec(Spec):
    class when_training_data_span_is_2_and_there_are_4_distinct_aggregates(Spec):
        def should_generate_errors_over_time_for_each_model(self):
            first_start_datetime = ['2016-05-16 09:00:00-04:00',
                    '2016-06-16 09:00:00-04:00',
                    '2016-07-16 09:00:00-04:00',
                    '2016-07-16 09:00:00-04:00',
                    '2016-08-16 09:00:00-04:00']
            l1_time = [9,10,9,9,9]
            l1_day = [0, 0,1,2,3]
            schedule_type = [1, 1,1,1,1]
            start_month = [5,6,7,7,8]
            start_year = [2016,2016,2016,2016,2016]
            user_tz = ['Brasilia',
                    'Brasilia',
                    'Pacific (US & Canada)',
                    'Pacific (US & Canada)',
                    'Pacific (US & Canada)'
                    ]
            args = {'l1_time': l1_time,
                    'l1_day': l1_day,
                    'schedule_type': schedule_type,
                    'first_start_datetime': first_start_datetime,
                    'start_month': start_month,
                    'start_year': start_year,
                    'user_tz': user_tz
                    }

            summaries = pd.DataFrame(args)
            summaries['first_start_datetime'] = pd.to_datetime(summaries['first_start_datetime'])

            bt = BackTest(data=summaries,
                    model=DumbModel,
                    training_data_span_months=2)
            error = bt.errors()
            expect('2016-6' not in error.index.values).to.equal(True)
            expect('2016-7' in error.index.values).to.equal(True)
            expect('2016-8' in error.index.values).to.equal(True)
    def should_generate_errors_over_time_for_each_model(self):
        first_start_datetime = ['2016-07-16 09:00:00-04:00',
                '2016-08-16 09:00:00-04:00']
        l1_time = [9,10]
        l1_day = [0, 0]
        schedule_type = [1, 1]
        start_month = [7,8]
        start_year = [2016,2016]
        user_tz = ['Brasilia', 'Brasilia']
        args = {'l1_time': l1_time,
                'l1_day': l1_day,
                'schedule_type': schedule_type,
                'first_start_datetime': first_start_datetime,
                'start_month': start_month,
                'start_year': start_year,
                'user_tz': user_tz
                }

        summaries = pd.DataFrame(args)
        summaries['first_start_datetime'] = pd.to_datetime(summaries['first_start_datetime'])

        bt = BackTest(data=summaries,
                model=DumbModel,
                training_data_span_months=1)
        error = bt.errors()
        expect('2016-8' in error.index.values).to.equal(True)
        expect('2016-7' not in error.index.values).to.equal(True)
        expect('2016-6' not in error.index.values).to.equal(True)
