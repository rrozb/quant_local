from unicodedata import name
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# FIXME add more generic plots

# TODO refactor + docs
# FIXME pass data in init


class CandleStickPlot:
    def __init__(self, indicator_columns=None) -> None:
        self.fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2])
        self.indicator_columns = indicator_columns

    def plot(self, data):
        self.fig.add_trace(
            go.Candlestick(x=data['date'],
                           open=data['open'],
                           high=data['high'],
                           low=data['low'],
                           close=data['close']),
            secondary_y=False,
        )
        if self.indicator_columns:
            self.add_indicator_trace(data, self.indicator_columns)
        return self.fig

    def add_indicator_trace(self, data, columns):
        for column in columns:
            self.fig.add_trace(go.Line(mode="lines",
                                       x=data["date"], y=data[column], name=column))
