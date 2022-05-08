import pandas as pd


class History:
    def __init__(self, data) -> None:
        self.data = data
        self.index = self.data.index
        # TODO change it
        # self.current_index = 1

    def get_snapshot(self, element_count=1) -> pd.DataFrame:
        return self.data.head(element_count)
