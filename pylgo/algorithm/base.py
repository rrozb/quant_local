from datetime import datetime
import pandas as pd
from ..data_loader import Loader, History
from ..portfolio import Portfolio, Position
from .time_simulation import TimeSimulation
from abc import ABC, abstractmethod
# TODO add multiple symbols.


class AlgorithmBase(ABC):
    def __init__(self, symbol=None, prefix=None, frequency=None, start=None, end=None, reporting_path=None, cash=10_000) -> None:
        self.symbol = symbol
        # Allow lower frequencies
        self.start = start
        self.end = end
        self.frequency = frequency
        self.prefix = prefix
        self.cash = cash
        self.portfolio = Portfolio(cash)
        self.reporting_path = reporting_path

    def map_signals(self, signals, data):
        # TODO here should be market data
        positions = []
        if not data.empty:
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
        simulation = TimeSimulation(
            self.frequency, self.start, self.end, history.last_point)
        while not simulation.stop():
            current_data = history.get_all_available_data(
                simulation.current_time)
            signals = self.create_signals(current_data)
            new_orders = self.map_signals(signals, current_data)
            self.portfolio.update(new_orders)
            simulation.update_current_timestamp()

        self.create_report()

    def create_report(self):
        # TODO make reporting object
        file_name = f'{self.reporting_path}/{self.symbol}_{self.frequency}_{self.start}_{self.end}_{int(datetime.now().timestamp())}.txt'
        with open(file_name, 'w+') as file:
            file.write(f'Total cash: {self.portfolio.cash}\n')
            file.write(
                f'Open positions value: {self.portfolio.positions_value}\n')
            file.write(
                f'Cash and positions value: {self.portfolio.cash + self.portfolio.positions_value}\n')
            file.write(
                f'Portfolio return: {self.portfolio.portfolio_return}\n')

    @abstractmethod
    def create_signals(self, data):
        pass
