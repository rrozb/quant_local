import datetime
import logging


class Portfolio:
    def __init__(self, cash):
        self.strating_cash = cash
        self.cash = cash
        self.positions = Positions()
        self.logger = logging.getLogger('portfolio testing')
        # TODO add metadata - like old positions, cash, fees etc.

    def manage(self, signals, data_collection):
        # TODO add order filling logic
        # acces data in better way than data.iloc[-1]['close']
        # TODO use better logic than avialabe_qnty.
        for singal in signals:
            current_price = data_collection[singal.symbol].iloc[-1]['close']
        # current_price = data.iloc[-1]['close']
        # avialabe_qnty = round(self.cash / current_price, 2)
        # self.logger.info('Available quantity: %s', avialabe_qnty)
        # # TODO refactor
        # if self.positions.active_positions is not None:
        #     self.update_position(
        #         self.positions.active_positions, current_price)
        # if signals.signal_type == 1:
        #     self.open_position(Position(
        #         signals.symbol, avialabe_qnty, current_price, data.iloc[-1]['date']))
        # elif signals.signal_type == 0:
        #     # FIXME SELECT SPECIFIC POSITION
        #     self.close_position(self.positions.active_positions)
        # self.logger.debug('Cash %s', self.cash)

    def open_position(self, position):
        # TODO add short position logic
        self.logger.info('Open position: %s', position)
        # TODO add position instead of just reset
        self.positions.active_positions = position
        self.cash = self.cash - position.value

    def close_position(self, position):
        self.logger.info('Close position: %s', position)
        self.positions.closed_positions.append(position)
        # TODO remove position instead of just reset
        self.positions.active_positions = None
        self.cash = self.cash + position.value

    def update_position(self, position, price, qnty=None):
        # FIXME correct position access
        self.positions.active_positions.current_price = price

    @ property
    def portfolio_return(self):
        return (self.positions.total_value - self.strating_cash)/self.strating_cash

    @ property
    def total_portfolio_value(self):
        return self.cash + self.positions.total_value


class Position:
    def __init__(self, symbol, quantity, start_price, time):
        self.symbol = symbol
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = time
        self.filled = False

    def __str__(self) -> str:
        return f'{self.time} {self.symbol}. Quantity {self.quantity} for a price {self.current_price}'

    @property
    def value(self):
        return self.quantity * self.current_price


class Positions:
    # TODO rewrite using named tuples.
    active_positions = None
    closed_positions = []
    logger = logging.getLogger('portfolio testing')

    @ property
    def total_value(self):
        return self.active_positions.current_price * self.active_positions.quantity
        # return sum([position.current_price for position in self.active_positions])

    @ property
    def active_positions_tickets(self):
        return self.active_positions.symbol
        # return [position.symbol for position in self.active_positions]
