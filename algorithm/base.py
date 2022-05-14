import pandas as pd
from data_loader import Loader, History
from portfolio import Portfolio, Position

from abc import ABC, abstractmethod
# TODO add multiple symbols.


class AlgorithmBase(ABC):
    def __init__(self, symbol=None, prefix=None, frequency=None, start=None, end=None, cash=10_000) -> None:
        self.symbol = symbol
        # Allow lower frequencies
        self.start = start
        self.end = end
        self.frequency = frequency
        self.prefix = prefix
        self.cash = cash
        self.portfolio = Portfolio(cash)

    def map_signals(self, signals, data):
        # TODO here should be market data
        positions = []
        price = data.iloc[-1]['close']
        for signal in signals:
            if self.symbol in [x.symbol for x in self.portfolio.active_positions]:
                self.portfolio.active_positions[0].current_price = price
            if signal.signal_type == 1:
                # TODO make generic
                qnty = self.cash / price
                positions.append(
                    Position(self.symbol, qnty, price))
        return positions

    def run(self):
        data = Loader(self.symbol,
                      self.frequency, self.start, self.end, self.prefix).load()
        history = History(data)
        # TODO optimize?
        for element_count, index_value in enumerate(history.index):
            current_data = history.get_snapshot(element_count)
            signals = self.create_signals(current_data)
            self.portfolio.update(self.map_signals(signals, current_data))

            # self.portfolio.update(signals, index_value)

    @abstractmethod
    def create_signals(self, data):
        pass
