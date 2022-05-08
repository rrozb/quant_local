import pandas as pd
import datetime


class Loader:
    def __init__(self, symbol, frequency, start=None, end=None) -> None:
        self.symbol = symbol
        # Allow lower frequencies
        self.start = datetime.datetime.strptime(
            start, '%Y-%m-%d %H:%M:%S') if start else None
        self.end = datetime.datetime.strptime(
            end, '%Y-%m-%d %H:%M:%S') if end else None
        self.frequency = frequency
        self.prefix = 'Bitfinex'

    def load(self):
        try:
            data = pd.read_csv(
                f'data/{self.prefix}_{self.symbol}_{self.frequency}.csv',
                index_col=0, parse_dates=True)
            data['date'] = pd.to_datetime(data['date'])
            if self.start:
                data = data[data.date > self.start]
            return data.sort_values(by='date', ascending=True)

        # FIXME add specific exceptions
        except Exception as e:
            raise Exception(e)
