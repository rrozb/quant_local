import pandas as pd
from ..alpha import Signal, SignalType


class Position:
    '''
    Active position.
    '''

    def __init__(self, signal: Signal, quantity, start_price, time, stop_loss, take_profit):
        self.signal = signal
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = time
        self.margin = 0
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def __str__(self) -> str:
        return f'{self.time} {self.signal.symbol}.' \
            + f'{self.signal.name} {self.signal.sign}' \
            + f'{self.quantity} for a price {self.current_price}'

    @property
    def stop_loss_hit(self):
        """
        Is stop loss hit.
        """
        if self.stop_loss is None:
            return False
        if self.signal.signal_type is SignalType.SELL:
            return ((self.start_price * self.quantity) -
                    (self.quantity * self.current_price)) \
                / ((self.start_price * self.quantity)) < -self.stop_loss
        return (self.quantity * self.current_price - self.quantity * self.start_price) \
            / (self.quantity * self.start_price) < -self.stop_loss

    @property
    def take_profit_hit(self):
        """
        Is stop loss hit.
        """
        if self.stop_loss is None:
            return False
        if self.signal.signal_type is SignalType.SELL:
            return ((self.start_price * self.quantity) -
                    (self.quantity * self.current_price)) \
                / ((self.start_price * self.quantity)) > self.take_profit
        return (self.quantity * self.current_price - self.quantity * self.start_price) \
            / (self.quantity * self.start_price) > self.take_profit

    @property
    def current_value(self):
        '''
        Current value of position.
        '''
        if self.signal.signal_type is SignalType.SELL:
            return (self.start_price * self.quantity) - (self.quantity * self.current_price)
        return self.quantity * self.current_price


class Positions:
    '''
    Colelction of positions.
    '''
    active_positions = []
    closed_positions = []

    def get_position(self, symbol):
        '''
        Get active positin by symbol.
        '''
        for position in self.active_positions:
            if position.signal.symbol == symbol:
                return position
        return None

    def remove_position(self, position: Position):
        '''
        Remove position from active positions.
        '''
        self.closed_positions.append(position)
        self.active_positions.remove(position)

    def add_position(self, position: Position):
        '''
        Add position to active positions.
        '''
        if position.signal.symbol not in self.active_positions_tickets:
            self.active_positions.append(position)
        else:
            raise Exception('Already exists.')

    @ property
    def total_value(self):
        '''Total value of positions.'''
        return sum(position.current_value for position in self.active_positions)

    @ property
    def active_positions_tickets(self):
        '''
        Tickets that have active position.
        '''
        return [position.signal.symbol for position in self.active_positions]

    def get_symbol_position(self, symbol) -> Position:
        '''
        Get position by symbol.
        '''
        if symbol not in self.active_positions_tickets:
            return None
        return [position for position in self.active_positions
                if position.signal.symbol == symbol][0]

    def history_to_pandas(self) -> pd.DataFrame:
        """
        Tranform closed positions to pandas.
        """
        data = []
        for position in self.closed_positions:
            data.append({
                'symbol': position.signal.symbol,
                'time': position.time,
                'start_price': position.start_price,
                'last_price': position.current_price,
                'quantity': position.quantity,
                # it shows price*quantity not net profit
                'position_value': position.current_value,
                'position_type': position.signal.signal_type.name
            })
        return pd.DataFrame(data)
