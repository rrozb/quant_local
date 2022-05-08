import pandas as pd
import datetime
from .portfolio import Portfolio
from data_loader import Loader
from .history import History
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

    def run(self):
        data = Loader(self.symbol,
                      self.frequency, self.start, self.end, self.prefix).load()
        history = History(data)
        # TODO optimize?
        for element_count, index_value in enumerate(history.index):
            self.create_sginals(history.get_snapshot(element_count))

    @abstractmethod
    def create_sginals(self, data):
        pass


class HODL(AlgorithmBase):
    def create_sginals(self, data):
        print('here')
