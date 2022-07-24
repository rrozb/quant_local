import logging
from ..alpha import Signal, SignalType


class Position:
    '''
    Active position.
    '''

    def __init__(self, signal: Signal, quantity, start_price, time):
        self.signal = signal
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = time
        self.margin = 0

    def __str__(self) -> str:
        return f'{self.time} {self.signal.symbol}.' \
            + f'{self.signal.name} {self.signal.sign}' \
            + f'{self.quantity} for a price {self.current_price}'

    @property
    def current_value(self):
        '''
        Current value of position.
        '''
        if self.signal.signal_type is SignalType.SELL:
            return (self.start_price * self.quantity) - (self.quantity * self.current_price)
        return self.quantity * self.current_price


class Positions:
    active_positions = []
    closed_positions = []
    logger = logging.getLogger('portfolio testing')

    def get_position(self, symbol):
        # TODO add cases when there are multiple postions for same symbol.
        for position in self.active_positions:
            if position.signal.symbol == symbol:
                return position
        return None

    def remove_position(self, position: Position):
        self.active_positions.remove(position)

    def add_position(self, position: Position):
        # TODO add duplicate check
        self.active_positions.append(position)

    @ property
    def total_value(self):
        return sum(position.current_value for position in self.active_positions)

    @ property
    def active_positions_tickets(self):
        return [position.signal.symbol for position in self.active_positions]

    def get_symbol_position(self, symbol) -> Position:
        # TODO allow multiple positions for same symbol
        if symbol not in self.active_positions_tickets:
            return None
        return [position for position in self.active_positions if position.signal.symbol == symbol][0]
