from datetime import datetime
from abc import ABC, abstractmethod
import logging
from typing import Dict
import pandas as pd
from ..data_loader import Loader
from ..portfolio import Portfolio
from .time_simulation import TimeSimulation
from ..plotting import CandleStickPlot

logger = logging.getLogger('algorithm testing')
logger.setLevel(logging.DEBUG)
logger_portfolio = logging.getLogger('portfolio testing')
logger_portfolio.setLevel(logging.DEBUG)
logger_positions = logging.getLogger('postitins testing')
logger_positions.setLevel(logging.DEBUG)


class AlgoStats:
    """
    Algorithms stats.
    """
    # TODO refactor it

    def __init__(self, reporting_path, base_file_name) -> None:
        self.base_file_name = base_file_name
        self.reporting_path = reporting_path
        self.stats = {
            'portfolio': []
        }
        self.data = None

    def save_to_csv(self) -> None:
        """
        Save stats to csv.
        """
        self.data.to_csv(
            f'{self.reporting_path}/metadata/{self.base_file_name}.csv')

    def transform_data(self) -> pd.DataFrame:
        """
        Transform data for saving.
        """
        data = pd.DataFrame(self.stats['portfolio'])
        data['date'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('date', inplace=True)
        data = data['portfolio_value']
        data = data.resample('D').ohlc(_method='ohlc')
        self.data = data
        return data


class AlgorithmLogging:
    '''
    Logging handler.
    '''
    # FIXME refactor.

    def __init__(self, symbols, logs_path, base_file_name):
        self.logs_path = f'{logs_path}/{base_file_name}.log'
        self.file_handler = logging.FileHandler(self.logs_path)
        self.file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        logger.addHandler(self.file_handler)
        logger.warning('Starting algorithm.')
        logger.warning('Available symbols are: %s', ', '.join(symbols))
        logger_portfolio.addHandler(self.file_handler)
        logger_positions.addHandler(self.file_handler)


class AlgorithmBase(ABC, AlgorithmLogging):
    '''
    Base algorithm.
    '''

    algo_name = None

    def __init__(self, symbols, prefix=None, frequency=None,
                 start=None, end=None, logs_path=None, reporting_path: str = None, cash=10_000) -> None:
        self.base_file_name = f'{self.algo_name}_{frequency}_{start}_{end}_{int(datetime.now().timestamp())}'
        super().__init__(symbols, logs_path, self.base_file_name)
        self.symbols = symbols
        self.start = start
        self.end = end
        self.frequency = frequency
        self.prefix = prefix
        self.cash = cash
        self.portfolio = Portfolio(cash)
        self.stats = AlgoStats(reporting_path, self.base_file_name)

    def __load_data(self):
        '''
        Load data from specified source.
        '''
        return Loader(self.symbols, self.frequency, self.start, self.end, self.prefix).load()

    def __is_empty(self, data: Dict[str, pd.DataFrame]):
        '''
        Check if collection is empty.
        '''
        return all(item.empty for item in data.values())

    def run(self):
        '''
        Run loop to iterate through history and simulate trades.
        '''
        data = self.__load_data()

        simulation = TimeSimulation(
            self.frequency, self.start, self.end, data.last_point)
        while not simulation.stop():
            current_data = data.get_snapshot(simulation.current_time)
            if not self.__is_empty(current_data):
                self.portfolio.manage(
                    list(self.create_signals(current_data)), current_data)
            self.stats.stats['portfolio'].append(
                {'timestamp': simulation.current_time, 'portfolio_value': self.portfolio.total_portfolio_value})
            simulation.update_current_timestamp()

    @abstractmethod
    def create_signals(self, current_data: Dict[str, pd.DataFrame]) -> None:
        '''
        Create signals that will be used to create trade orders.
        '''

    def __del__(self):
        logger.info('Algorithm finished %s.', self.algo_name)
        logger.info('Total cash: %s', self.portfolio.cash)
        logger.info('Total value: %s',
                    self.portfolio.total_portfolio_value)
        logger.info('Total return: %s', self.portfolio.portfolio_return)
        # FIXME
        ####
        data = self.stats.transform_data()
        self.stats.save_to_csv()
        # TODO refactor
        self.portfolio.positions.history_to_pandas().to_csv(
            f'reports/metadata/{self.base_file_name}_positions.csv')
        ###
        graph = CandleStickPlot()
        data.reset_index(inplace=True)
        graph.plot(data)
        graph.fig.show()
