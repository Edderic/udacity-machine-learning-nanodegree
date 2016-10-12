import pandas as pd

class Validation():
    def __init__(self, data_df):
        self._data_df = data_df

    def num_months(self):
        return self.size().shape[0]

    def size(self):
        return self._data_df.groupby(['start_year', 'start_month']).size()

    def training_data(self, i, length):
        td = pd.DataFrame()
        for x in range(i, i+length):
            year, month = self.size().index[x]
            new_df = self._data_df[(self._data_df['start_year'] == year)\
                    & (self._data_df['start_month'] == month)]
            td = td.append(new_df)

        return td

    def year_month_index(self, i):
        year, month = self.size().index[i]
        return "{}-{}".format(year, month)

    def test_data(self, i):
        year, month = self.size().index[i]
        return self._data_df[(self._data_df['start_year'] == year) \
                & (self._data_df['start_month'] == month)]

