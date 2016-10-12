import pickle
import pandas as pd
import sys, os

sys.path.append(os.path.join(os.getcwd(), 'code'))

from backtest import BackTestMultiple
from models import InterpolatedProbModel,\
    SmartHeuristicModel, \
    DumbModel,\
    TimezoneProbModel,\
    LFProbModel,\
    LFTProbModel,\
    GeneralProbModel
    # OptimizedTimezoneProbModel,\

df = pickle.load(open('unique_user_summaries.pkl'))
data_df = df[df['user_tz'].notnull()]

# models = [ProbModel, ScheduleTypeOnly, DumbModel, SmartHeuristicModel]
models = [ InterpolatedProbModel,
             LFTProbModel,\
             LFProbModel,\
             TimezoneProbModel,\
             GeneralProbModel,\
             SmartHeuristicModel,\
             DumbModel]
 # OptimizedTimezoneProbModel,\

errors_df = pd.DataFrame()

training_data_span_months = 18


b = BackTestMultiple(models=models, data=data_df, training_data_span_months=18)
err = b.errors()
pickle.dump(err, open('x_model_errors.pkl', 'wb'))


