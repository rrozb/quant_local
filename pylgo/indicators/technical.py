class MovingAverage:
    @staticmethod
    def calculate(data, column_name, period):
        return data[column_name].rolling(window=period).mean()
# TODO add MACD
