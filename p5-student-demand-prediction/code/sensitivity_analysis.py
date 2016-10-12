import pickle
import pandas as pd
import sys, os
import datetime

sys.path.append(os.path.join(os.getcwd(), 'code'))

from backtest import BackTest, BackTestMultiple
from models import SmartHeuristicModel, \
    DumbModel,\
    InterpolatedProbModel,\
    OptimizedTimezoneProbModel,\
    TimezoneProbModel,\
    LFProbModel,\
    LFTProbModel,\
    GeneralProbModel

df = pickle.load(open('unique_user_summaries.pkl'))
data_df = df[df['user_tz'].notnull()]

# models = [LFTProbModel,\
    # LFProbModel,\
    # OptimizedTimezoneProbModel,\
    # TimezoneProbModel,\
    # GeneralProbModel,\
    # SmartHeuristicModel,\
    # DumbModel]
#
# Main idea:
# We would like to compare GeneralProbModel and TimezoneProbModel.
# We want to see how it responds to underrepresented data.
# Two generally good assumptions based on performance so far on real data:
# Pick a timezone that is represented but weird
# For each, copy the data but just change the timezone!

# Generate schedules following a distribution for two months
# For each distribution:
#   Append it to the data
#   Calculate errors for the two months with fake-generated data
# Discuss for each scenario how the models performed

#
# Get an under-represented timezone (ur_tz).
ur_tz = df.groupby('user_tz').size().sort_values().index[0]

def get_latest_year_month(df):
    max_start_year = df.start_year.max()
    max_start_month = df[df.start_year == max_start_year].start_month.max()
    return (max_start_year, max_start_month)

def gen_random_sched(timezone, user_schedules):
    # get the latest date
    max_sy, max_sm = get_latest_year_month(user_schedules)
    dt = datetime.datetime(max_sy, max_sm, 1, 0, 0, 0)
    new_dt = dt + datetime.timedelta(days=31)

    new_sy = new_dt.year
    new_sm = new_dt.month

    fake_data = user_schedules[(user_schedules.start_month == 7) &\
            (user_schedules.start_year == 2016)].copy()

    fake_data['user_tz'] = timezone
    fake_data['start_year'] = new_sy
    fake_data['start_month'] = new_sm

    return fake_data


def append_sched_with_fake(timezone, df):
    cp = df.copy()
    random_sched_1 = gen_random_sched(timezone, df)
    cp1 = cp.append(random_sched_1, ignore_index=True)

    random_sched_2 = gen_random_sched(timezone, cp1)

    return cp1.append(random_sched_2, ignore_index=True)



models = [InterpolatedProbModel, TimezoneProbModel, GeneralProbModel]
# TODO: be able to specify in terms of test data, not training data
training_data_span_months = 32
b = BackTestMultiple(data=append_sched_with_fake(ur_tz, df),
        models=models,
        training_data_span_months=training_data_span_months)
err = b.errors()
print err

pickle.dump(err, open('data/sensitivity_analysis.pkl', 'wb'))

