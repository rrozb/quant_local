from typing import Dict
import pandas as pd


class History:
    '''
    History object for specific symbol.
    '''

    def __init__(self, data) -> None:
        self.data = data.sort_index()

    def get_all_available_data(self, current_timestamp) -> pd.DataFrame:
        '''
        Get all available data for History.
        '''
        return self.data[self.data.index <= current_timestamp]

    @property
    def size(self):
        """
        Size of history
        """
        return self.data.index[0]

    def get_value(self, column: str, position=0):
        """
        Get value from history.
        """
        if column == 'timestamp_index':
            return self.data.index[position]
        return self.data.iloc[position][column]


class HistorySnapshot(History):
    """
    Snapshot of available history.
    """

    def __init__(self, data) -> None:
        super().__init__(data)
        self.data = data


class HistoryCollection:
    '''
    Collection of History objects.
    '''

    collection = {}

    @property
    def last_point(self) -> int:
        '''
        Get lates value from colelction.
        '''
        return max((history.get_value('timestamp_index', -1)
                    for history in self.collection.values()))

    def get_snapshots(self, current_timestamp: int) -> Dict[str, pd.DataFrame]:
        '''
        Get snapshot of history.
        '''
        return {symbol: HistorySnapshot(history.get_all_available_data(current_timestamp))
                for symbol, history in self.collection.items()}
