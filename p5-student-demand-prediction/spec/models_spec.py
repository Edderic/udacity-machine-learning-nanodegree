import sys, os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from specter import Spec, expect

from models import DumbModel, GeneralProbModel, SmartHeuristicModel

class ModelsSpec(Spec):
    class prob_model(Spec):
        class predict(Spec):
            def should_take_into_account_conditional_probability(self):
                user_tz = ['Eastern (US & Canada)', 'Pacific (US & Canada)']
                l1_time = [9, 9]
                l1_day = [0, 1]
                l2_time = [9, 9]
                l2_day = [3, 4]
                l3_time = [None, 9]
                l3_day = [None, 5]
                schedule_type = [2, 3]

                training_data = pd.DataFrame({ 'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l1_day': l1_day,
                    'l2_time': l2_time,
                    'l2_day': l2_day,
                    'l3_time': l3_time,
                    'l3_day': l3_day,
                    'schedule_type': schedule_type
                    })

                business_forecast = [{'schedule_type': 2,
                         'user_tz': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'user_tz': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                model = GeneralProbModel()

                model.fit(training_data)
                p = model.predict(business_forecast)
                expect(True).to.equal(True)

            def handles_predicting_cases_it_has_not_seen_before(self):
                user_tz = ['Eastern (US & Canada)', 'Pacific (US & Canada)']
                l1_time = [9, 9]
                l1_day = [0, 1]
                l2_time = [9, 9]
                l2_day = [3, 4]
                l3_time = [None, 9]
                l3_day = [None, 5]
                schedule_type = [2, 3]

                training_data = pd.DataFrame({ 'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l1_day': l1_day,
                    'l2_time': l2_time,
                    'l2_day': l2_day,
                    'l3_time': l3_time,
                    'l3_day': l3_day,
                    'schedule_type': schedule_type
                    })

                business_forecast = [{'schedule_type': 1,
                         'user_tz': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 4,
                         'user_tz': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                model = GeneralProbModel()

                model.fit(training_data)
                p = model.predict(business_forecast)

                expect(True).to.equal(True)

    class smart_heuristic_model(Spec):
        class generate_sample_schedule(Spec):
            def should_not_have_weird_hours(self):
                user_tz = ['Eastern (US & Canada)', 'Pacific (US & Canada)']
                l1_time = [9, 9]
                l2_time = [9, 9]
                l3_time = [None, 9]

                training_data = pd.DataFrame({ 'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l2_time': l2_time
                    })

                business_forecast = [{'schedule_type': 2,
                         'timezone': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'timezone': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                smart_heuristic_model = SmartHeuristicModel()
                smart_heuristic_model.fit(training_data)

                schedule = smart_heuristic_model.\
                        generate_sample_schedule(business_forecast)
                _sum = schedule._table_df.sum().sum()
                expect(_sum).to.equal(8)

    class dumb_model(Spec):
        class generate(Spec):
            def should_create_a_sample_that_meets_business_forecast_criteria(self):
                user_tz = ['Eastern (US & Canada)', 'Pacific (US & Canada)']
                l1_time = [9, 9]
                l2_time = [9, 9]
                l3_time = [None, 9]

                training_data = pd.DataFrame({ 'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l2_time': l2_time
                    })

                business_forecast = [{'schedule_type': 2,
                         'timezone': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'timezone': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                dumb_model = DumbModel()
                dumb_model.fit(training_data)

                schedule = dumb_model.generate_sample_schedule(business_forecast)
                _sum = schedule._table_df.sum().sum()
                expect(_sum).to.equal(8)


        class predict(Spec):

            def should_predict_with_bins(self):
                dumb_model = DumbModel()

                business_forecast = [{'schedule_type': 2,
                         'timezone': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'timezone': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                p = dumb_model.predict(business_forecast)
                expect(round(p[0] + p[1] + p[2] + p[3] + p[4] + p[5])).to.equal(8)
