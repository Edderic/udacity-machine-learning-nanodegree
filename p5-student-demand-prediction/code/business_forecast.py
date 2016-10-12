class BusinessForecast():
    def __init__(self, data_df):
        self._data_df = data_df

    def convert(self):
        freqs = self._data_df.groupby(['schedule_type','user_tz']).size()

        forecasts = []

        for schedule_type, user_tz in freqs.index:
            entry = {'schedule_type': schedule_type,
                    'user_tz': user_tz,
                    'frequency': freqs[schedule_type][user_tz]}
            forecasts.append(entry)

        return forecasts
