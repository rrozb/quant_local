import plotly.graph_objects as go
from plotly.subplots import make_subplots


class CandleStickPlot:
    """
    Create candle plot
    """

    def __init__(self, indicator_columns=None, algo_name=None) -> None:
        self.fig = make_subplots(
            rows=2, cols=1, row_heights=[0.8, 0.2])
        self.indicator_columns = indicator_columns
        self.algo_name = algo_name

    def plot(self, data):
        """
        Plot candle stick chart
        """
        self.fig.add_trace(
            go.Candlestick(x=data['date'],
                           open=data['open'],
                           high=data['high'],
                           low=data['low'],
                           close=data['close'])
        )
        if self.indicator_columns:
            self.add_indicator_trace(data, self.indicator_columns)
        self.fig.update_layout(
            title=self.algo_name,
            xaxis_title="date",
            yaxis_title="Portfolio value",
            xaxis_rangeslider_visible=False,
        )
        return self.fig

    def add_indicator_trace(self, data, columns):
        """
        Add traces with indicators.
        """
        for column in columns:
            self.fig.add_trace(go.Line(mode="lines",
                                       x=data["date"], y=data[column], name=column))
