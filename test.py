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

fig = CandleStickPlot(
    indicator_columns=['MA12', 'MA26', 'MA50', 'MA100']).plot(data)
fig.show()
