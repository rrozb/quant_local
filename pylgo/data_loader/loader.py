import datetime

from engine.db import CandlesRepo
#import pandas as pd

from .data_model import History, HistoryCollection
import requests
import pytz
import time
from datetime import datetime

class Loader:
    '''
    Loader for getting data from local storage.
    '''

    def __init__(self, symbols, frequency, start=None, end=None, prefix='Bitfinex',) -> None:
        self.symbols = symbols
        self.start = datetime.datetime.strptime(
            start, '%Y-%m-%d %H:%M:%S') if start else None
        self.end = datetime.datetime.strptime(
            end, '%Y-%m-%d %H:%M:%S') if end else None
        self.frequency = frequency
        self.prefix = prefix

    def load(self):
        '''
        Load dataset.
        '''
        try:
            history_collection = HistoryCollection()
            for symbol in self.symbols:
                data = pd.read_csv(
                    f'pylgo/data/{self.prefix}_{symbol}_{self.frequency}.csv',
                    index_col=0, parse_dates=True)
                data['date'] = pd.to_datetime(data['date'])
                if self.start:
                    data = data[data.date > self.start]
                history_collection.collection[symbol] = History(data.sort_values(
                    by='date', ascending=True))
            return history_collection
        # FIXME add specific exceptions
        except Exception as e:
            raise Exception(e)

#TODO Add timeframe to BitFInexLoaderAPI
TIMEFRAME = {
    "1m":"60000",
    "5m": "300000",
    '15m': "900000",
    '30m': '1800000',
    '1h': '3600000',
    '3h': '10800000',
    '6h': '21600000',
    '12h': '43200000',
    '1D': '86400000',
    '1W': '604800000',
    '14D': '1209600000',
    '1M': '2592000000'

}
class BitfinexLoaderAPI():
    """
    Class to work with Bitfinex API
    """
    def __init__(self, symbol: str, start_date: datetime, end_date: datetime, timeframe: str = None, **kwargs) -> None:
        self.baseUrl = "https://api-pub.bitfinex.com/v2/candles/trade:1m:"
        self.symbol = symbol
        self.start_date = datetime.strptime(
            start_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
        self.end_date = datetime.strptime(
            end_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
        self.timestep = 10000 * 60000
        self.start_date_unix = self.start_date.timestamp() * 1000
        self.end_date_unix = self.end_date.timestamp() * 1000      

    def get_data(self) -> None:
        """
        Get current date
        """
        current_time = self.start_date_unix
        while current_time < self.end_date_unix:
            if self.end_date_unix - current_time > self.timestep:
                self.send_request(start=current_time, end=current_time+self.timestep)
                current_time += self.timestep
            else:
                self.send_request(start=current_time, end=self.end_date_unix)
                current_time = (self.end_date_unix - current_time) + current_time

    def send_request(self, start: int, end: int) -> None:
        """
        Send request to Bitfinex API with current date
        """
        r = requests.get(f'{self.baseUrl}{self.symbol}/hist?start={start}&end={end}&limit=10000')
        if r.status_code == 200:
            for candle in r.json():
                CandlesRepo.create(candles=candle, symbol=self.symbol)           
        if r.status_code == 429:
            print('You have reached ratelimit. Waiting 1 minute...')
            time.sleep(60)
            r = requests.get(f'{self.baseUrl}{self.symbol}/hist?start={start}&end={end}&limit=10000')


