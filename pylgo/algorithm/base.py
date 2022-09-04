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

    def __init__(self, reporting_path, base_file_name) -> None:
        self.base_file_name = base_file_name
        self.reporting_path = reporting_path
        self.stats = {
            'portfolio': []
        }
        self.portfolio_data = None
        self.positions_report = None

    def __prepare_positions_report(self):
        """
        Prepare positions data for report.
        """

        transactions_number = len(self.stats['positions'])

        positions_report = f'''Number of transactions: {transactions_number}
        '''
        return positions_report

    def __prepare_portfolio_data(self):
        """
        Transform portfolio data into OHLC format.
        """
        data = pd.DataFrame(self.stats['portfolio'])
        data['date'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('date', inplace=True)
        data = data['portfolio_value'].resample('D').ohlc(_method='ohlc')
        # reset index to have date as normal column
        data.reset_index(inplace=True)
        return data

    def prepare_data(self):
        """
        Prepare reporting data
        """
        self.portfolio_data = self.__prepare_portfolio_data()
        self.positions_report = self.__prepare_positions_report()

    def save(self):
        """
        Save data and report locally.
        """
        self.portfolio_data.to_csv(
            f'{self.reporting_path}/metadata/portfolio_{self.base_file_name}.csv')
        self.stats['positions'].to_csv(
            f'{self.reporting_path}/metadata/positions_{self.base_file_name}.csv')
        with open(f'{self.reporting_path}/metadata/report_{self.base_file_name}.txt',
                  'w+', encoding='UTF-8') as f:
            f.write(self.positions_report)


class AlgorithmLogging:
    '''
    Logging handler.
    '''

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
                 start=None, end=None, logs_path=None,
                 reporting_path: str = None, cash=10_000) -> None:
        self.base_file_name = f'{self.algo_name}_{frequency}_{start}_{end}_{int(datetime.now().timestamp())}'
        super().__init__(symbols, logs_path, self.base_file_name)
        self.symbols = symbols
        self.start = start
        self.end = end
        self.frequency = frequency
        self.prefix = prefix
        self.cash = cash
        self.portfolio = Portfolio(cash)
        # TODO rename it
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
        return all(item.data.empty for item in data.values())

    def pre_run(self):
        """
        Function to be called before run.
        """
        return

    def run(self):
        '''
        Run loop to iterate through history and simulate trades.
        '''
        self.pre_run()
        data = self.__load_data()

        simulation = TimeSimulation(
            self.frequency, self.start, self.end, data.last_point)
        while not simulation.stop():
            snapshot = data.get_snapshots(simulation.current_time)
            if not self.__is_empty(snapshot):
                self.portfolio.manage(
                    list(self.create_signals(snapshot)), snapshot)
            self.stats.stats['portfolio'].append(
                {'timestamp': simulation.current_time,
                    'portfolio_value': self.portfolio.total_portfolio_value})
            simulation.update_current_timestamp()
        self.stats.stats['positions'] = self.portfolio.positions.history_to_pandas()
        logger.info('Algorithm finished %s.', self.algo_name)
        logger.info('Total cash: %s', self.portfolio.cash)
        logger.info('Total value: %s',
                    self.portfolio.total_portfolio_value)
        logger.info('Total return: %s', self.portfolio.portfolio_return)

        self.stats.prepare_data()
        graph = CandleStickPlot(algo_name=self.algo_name)
        graph.plot(self.stats.portfolio_data)
        graph.fig.show()
        self.stats.save()
        self.close()

    def close(self):
        """
        After algorithm was run.
        """
        logger.info('Algorithm finished %s.', self.algo_name)
        logger.info('Total cash: %s', self.portfolio.cash)
        logger.info('Total value: %s',
                    self.portfolio.total_portfolio_value)
        logger.info('Total return: %s', self.portfolio.portfolio_return)

        self.stats.prepare_data()
        graph = CandleStickPlot(algo_name=self.algo_name)
        graph.plot(self.stats.portfolio_data)
        graph.fig.show()
        self.stats.save()

    @abstractmethod
    def create_signals(self, current_data: Dict[str, pd.DataFrame]) -> None:
        '''
        Create signals that will be used to create trade orders.
        '''
