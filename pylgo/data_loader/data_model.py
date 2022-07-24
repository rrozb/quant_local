import pandas as pd


class History:
    '''
    History object for specific symbol.
    '''

    def __init__(self, data) -> None:
        self.data = data.sort_index()
        self.index = self.data.index
        self.first_point = self.index[0]
        self.last_point = self.index[-1]

    def get_all_available_data(self, current_timestamp) -> pd.DataFrame:
        '''
        Get all available data for History.
        '''
        return self.data[self.index <= current_timestamp]


class HistoryCollection:
    '''
    Collection of History objects.
    '''
    collection = {}

    @property
    def last_point(self):
        '''
        Get lates value from colelction.
        '''
        return max([history.last_point for history in self.collection.values()])

    def get_snapshot(self, current_timestamp):
        '''
        Get snapshot of history.
        '''
        return {symbol: history.get_all_available_data(current_timestamp)
                for symbol, history in self.collection.items()}
