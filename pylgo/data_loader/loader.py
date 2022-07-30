import datetime
import pandas as pd
from .data_model import History, HistoryCollection


class Loader:
    '''
    Loader for getting data from local storage.
    '''

    def __init__(self, symbols, frequency, start=None, end=None, prefix='Bitfinex',) -> None:
        self.symbols = symbols
        self.start = datetime.datetime.strptime(
            start, '%Y-%m-%d %H:%M:%S') if start else None
        self.end = datetime.datetime.strptime(
            end, '%Y-%m-%d %H:%M:%S') if end else None
        self.frequency = frequency
        self.prefix = prefix

    def load(self):
        '''
        Load dataset.
        '''
        try:
            history_collection = HistoryCollection()
            for symbol in self.symbols:
                data = pd.read_csv(
                    f'pylgo/data/{self.prefix}_{symbol}_{self.frequency}.csv',
                    index_col=0, parse_dates=True)
                data['date'] = pd.to_datetime(data['date'])
                if self.start:
                    data = data[data.date > self.start]
                history_collection.collection[symbol] = History(data.sort_values(
                    by='date', ascending=True))
            return history_collection
        # FIXME add specific exceptions
        except Exception as e:
            raise Exception(e)
