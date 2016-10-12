import sys, os
import pandas as pd
from specter import Spec, expect
from timezone import Timezone
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))
from business_forecast import BusinessForecast

class BusinessForecastSpec(Spec):
    class given_data(Spec):
        def should_generate_a_bunch_of_types(self):
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

            bf = BusinessForecast(unique_user_summaries)
            forecasts = bf.convert()
            expect(len(forecasts)).to.equal(3)
