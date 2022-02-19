import plotly.graph_objects as go
from plotly.subplots import make_subplots
# FIXME add more generic plots


class CandleStickPlot:
    def __init__(self) -> None:
        pass

    def plot(self, data):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Candlestick(x=data['date'],
                           open=data['open'],
                           high=data['high'],
                           low=data['low'],
                           close=data['close']),
            secondary_y=False,
        )

        return fig

    # fig.show()
