from sklearn.metrics import mean_squared_error, mean_absolute_error
from business_forecast import BusinessForecast
from schedule import ActualSchedule
from validation import Validation
import numpy as np
import pandas as pd

class BackTest():
    def __init__(self,
            data=None,
            model=None,
            training_data_span_months=1):
        self._data_df = data
        self._model = model
        self.training_data_span_months = training_data_span_months
        self.validation = Validation(data)

    def errors(self):
        indices = [] # index of a row, formatted YYYY-M (e.g. 2016-8, 2016-9)
        predictions = []
        errors = [] # errors. Lower is better
        test_data_size = []
        actuals = []

        for i in range(0,self.num_months()-self.training_data_span_months):
            m = self._model()
            training_data = self.training_data(i, self.training_data_span_months)
            m.fit(training_data)

            td = self.test_data(i+self.training_data_span_months)

            print "Generating prediction..."
            prediction = m.predict(\
                    BusinessForecast(\
                    td).convert(),
                    training_data=training_data)

            actual = ActualSchedule(\
                    td).bins()

            print "prediction "
            print prediction
            print "\n"

            print "actual"
            print actual
            print "\n"

            error = mean_absolute_error(actual, prediction)
            errors.append(error)

            index = self.year_month_index(i+self.training_data_span_months)
            indices.append(index)
            print "time: {}, error: {}".format(index, error)

            predictions.append(prediction)
            actuals.append(actual)
            test_data_size.append(actual.sum())

        return pd.DataFrame({
            'errors': errors,
            'test_data_size': test_data_size,
            'predictions': predictions,
            'actuals': actuals
            }).set_index([indices])

    #private
    def size(self):
        return self.validation.size()

    def num_months(self):
        return self.validation.num_months()

    def training_data(self, *args):
        return self.validation.training_data(*args)

    def year_month_index(self, *args):
        return self.validation.year_month_index(*args)

    def test_data(self, *args):
        return self.validation.test_data(*args)


class BackTestMultiple():
    def __init__(self, models=[], data=pd.DataFrame(), training_data_span_months=0):
        self.models = models
        self.data = data[self.relevant_columns()]
        self.training_data_span_months = training_data_span_months

    def errors(self):
        errors_df = pd.DataFrame()

        for index, model in enumerate(self.models):
            print "Back-testing {} with {} months of training data...".format(model.__name__,
                    self.training_data_span_months)
            b = BackTest(model=model,
                    data=self.data,
                    training_data_span_months=self.training_data_span_months)
            model_error = b.errors()

            errors_df[model.__name__] = model_error['errors']
            errors_df['{}_predictions'.format(model.__name__)] = model_error['predictions']

            if index == len(self.models) - 1:
                errors_df['test_data_size'] = model_error['test_data_size']
                errors_df['actuals'] = model_error['actuals']

        print "errors_df"
        print errors_df
        print "\n"

        return errors_df

    def relevant_columns(self):
        return ['user_tz',
                'schedule_type',
                'l1_time',
                'l1_day',
                'l2_time',
                'l2_day',
                'l3_time',
                'l3_day',
                'l4_time',
                'l4_day',
                'l5_time',
                'l5_day',
                'l6_time',
                'l6_day',
                'l7_time',
                'l7_day',
                'start_year',
                'start_month',
                ]
