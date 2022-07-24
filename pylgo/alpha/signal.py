import datetime
from enum import Enum


class SignalType(Enum):
    '''
    Types of signals
    '''
    LIQUIDATE = 0
    BUY = 1
    SELL = 2


class Signal:
    '''
    Signal for opening position.
    '''

    def __init__(self, signal_type: SignalType, symbol: str, execute_at: datetime = None) -> None:
        self.signal_type = signal_type
        self.created_at = datetime.datetime.now()
        self.symbol = symbol
        self.execute_at = execute_at

    @property
    def sign(self):
        '''
        Get sign for signal.
        '''
        if self.signal_type is SignalType.SELL:
            return '-'
        return ''

    @property
    def name(self):
        '''
        Get signals name
        '''
        return self.signal_type.name
    