import imp
from data_loader import Loader
import plotly.graph_objects as go
from plotting import CandleStickPlot
data = Loader(symbol='ETHUSD', start='2022-01-01 06:00:00',
              frequency='1h').load()
data['MA12'] = data['close'].rolling(window=12).mean()
data['MA4'] = data['close'].rolling(window=4).mean()
data['MA24'] = data['close'].rolling(window=24).mean()

data['std12'] = data['close'].rolling(window=12).std()
data['std4'] = data['close'].rolling(window=4).std()
data['std24'] = data['close'].rolling(window=24).std()

fig = CandleStickPlot().plot(data)

fig.add_trace(go.Line(mode="lines",
              x=data["date"], y=data["MA12"], name="MA12"))
fig.add_trace(go.Line(mode="lines",
              x=data["date"], y=data["MA4"], name="MA4"))
fig.add_trace(go.Line(mode="lines",
              x=data["date"], y=data["MA24"], name="MA24"))

# fig.add_trace(go.Line(mode="lines",
#               x=data["date"], y=data["std12"], name="std12"), secondary_y=True,)
# fig.add_trace(go.Line(mode="lines",
#               x=data["date"], y=data["std4"], name="std4"), secondary_y=True,)
# fig.add_trace(go.Line(mode="lines",
#               x=data["date"], y=data["std24"], name="std24"), secondary_y=True,)

fig.show()
