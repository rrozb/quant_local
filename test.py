from indicators import MovingAverage
from data_loader import Loader
import plotly.graph_objects as go
from plotting import CandleStickPlot
data = Loader(symbol='ETHUSD', start='2022-01-01 06:00:00',
              frequency='1h').load()
moving_average_indicator = MovingAverage()
data['MA12'] = moving_average_indicator.calculate(data, 'close', 12)
data['MA26'] = moving_average_indicator.calculate(data, 'close', 26)
data['MA50'] = moving_average_indicator.calculate(data, 'close', 50)
data['MA100'] = moving_average_indicator.calculate(data, 'close', 100)

data['MACD'] = data['MA50'] - data['MA100']
data['signal'] = data['MACD'].rolling(window=9).mean()


fig = CandleStickPlot(
    indicator_columns=['MA12', 'MA26', 'MA50', 'MA100']).plot(data)

# TODO MACD graph. Move to plotting.
# fig.add_trace(go.Scatter(
#     x=data['date'], y=data['signal'], name='signal',), row=2, col=1)
# fig.add_trace(go.Bar(
#     x=data['date'],
#     y=data['MACD'],
#     name='MACD',
# ), row=2, col=1)

fig.show()
