from datetime import datetime
import logging
import pandas as pd
from ..data_loader import Loader, History
from ..portfolio import Portfolio, Position
from .time_simulation import TimeSimulation
from abc import ABC, abstractmethod
# TODO add multiple symbols.
# TODO add confifuration file
logger = logging.getLogger('algorithm testing')
logger.setLevel(logging.DEBUG)
logger_portfolio = logging.getLogger('portfolio testing')
logger_portfolio.setLevel(logging.DEBUG)
logger_positions = logging.getLogger('postitins testing')
logger_positions.setLevel(logging.DEBUG)
# TODO add other with https://docs.python.org/3/howto/logging-cookbook.html


class AlgorithLogging:
    def __init__(self, algo_name, symbols, frequency, start, end, reporting_path):
        self.reporting_path = f'{reporting_path}/{algo_name}_{frequency}_{start}_{end}_{int(datetime.now().timestamp())}.txt'
        self.file_handler = logging.FileHandler(self.reporting_path)
        self.file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        logger.addHandler(self.file_handler)
        logger.warning('Starting algorithm.')
        logger.warning('Available symbols are: %s', ', '.join(symbols))
        logger_portfolio.addHandler(self.file_handler)
        logger_positions.addHandler(self.file_handler)


class AlgorithmBase(ABC, AlgorithLogging):
    algo_name = None
    # TODO make no default values like frequenct start etc.

    def __init__(self, symbols, prefix=None, frequency=None,
                 start=None, end=None, reporting_path=None, cash=10_000) -> None:
        super().__init__(self.algo_name, symbols, frequency, start, end, reporting_path)
        self.symbols = symbols
        self.start = start
        self.end = end
        self.frequency = frequency
        self.prefix = prefix
        self.cash = cash
        self.portfolio = Portfolio(cash)

    def __load_data(self):
        # TODO add validation for symbols
        return Loader(self.symbols, self.frequency, self.start, self.end, self.prefix).load()

    def __get_current_data(self, data_collection, current_timestamp):
        data_collection_snapshot = {}
        for symbol, all_data in data_collection.items():
            data_collection_snapshot[symbol] = all_data.get_all_available_data(
                current_timestamp)
        return data_collection_snapshot

    def run(self):
        data = self.__load_data()
        # TODO refactor after adding model
        first_elem = next(iter(data))
        last_point = data[first_elem].last_point
        ###
        simulation = TimeSimulation(
            self.frequency, self.start, self.end, last_point)
        while not simulation.stop():
            # FIXME multiple
            current_data = self.__get_current_data(data,
                                                   simulation.current_time)
            signals = self.create_signals(current_data)
            # TODO current data >>> use only prices not entire dataset.
            if signals is not None:
                self.portfolio.manage(signals, current_data)
            simulation.update_current_timestamp()
        logger.info('Algorithm finished %s.', self.algo_name)
        logger.info('Total cash: %s', self.portfolio.cash)
        logger.info('Total value: %s', self.portfolio.total_portfolio_value)
        logger.info('Total return: %s', self.portfolio.portfolio_return)

    @abstractmethod
    def create_signals(self, data):
        pass
