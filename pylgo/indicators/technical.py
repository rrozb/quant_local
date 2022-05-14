# class TechnicalBase:
#     def __init__(self, data, column_name):
#         self.data = data
#         self.column_name = column_name


class MovingAverage:
    @staticmethod
    def calculate(data, column_name, period):
        return data[column_name].rolling(window=period).mean()
    # def add_moving_average(self, window):
    #     self.data[f'MA{window}'] = self.data[self.column_name].rolling(
    #         window=window).mean()
    #     return self.data

# TODO add MACD
