import pandas as pd


class History:
    def __init__(self, data) -> None:
        self.data = data.sort_index()
        self.index = self.data.index
        self.first_point = self.index[0]
        self.last_point = self.index[-1]
    # TODO consider bathces if needed due to performance.

    def get_all_available_data(self, current_timestamp) -> pd.DataFrame:
        return self.data[self.index <= current_timestamp]
