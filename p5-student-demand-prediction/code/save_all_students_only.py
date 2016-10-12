import pandas as pd
from dateutil.parser import parse
import pickle


def filter_for_all_students(df):
    mask = df.company_name == 'all_students'
    return df[mask]

name = 'data/export_lesson_requests_2016-09-08T07:50:31-04:00'
all_df = pd.read_csv(name,\
        parse_dates=['lr_start_datetime'],\
        date_parser=parse,\
        na_values="",\
        dtype={'user_id': 'str', 'lr_id': 'str', 'cr_id': 'str'}\
        )

lesson_request_data = filter_for_all_students(all_df)

pickle.dump(lesson_request_data, open('data/export_lesson_requests_2016_09_08.pkl', 'wb'))


