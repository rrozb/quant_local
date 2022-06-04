import datetime
import logging


class Portfolio:
    def __init__(self, cash):
        self.strating_cash = cash
        self.cash = cash
        self.positions = Positions()
        self.logger = logging.getLogger('portfolio testing')

    def manage(self, signals, data):
        # TODO add order filling logic
        # acces data in better way than data.iloc[-1]['close']
        # TODO use better logic than avialabe_qnty.
        avialabe_qnty = self.cash / data.iloc[-1]['close']
        self.logger.info('Available quantity: %s', avialabe_qnty)
        if signals.signal_type == 1:
            self.open_position(Position(
                signals.symbol, avialabe_qnty, data.iloc[-1]['close']))
        # elif signals.signal_type == -1:
        #     self.positions.active_positions = Position(
        #         signals.symbol, -avialabe_qnty, data.iloc[-1]['close'])
        elif signals.signal_type == 0:
            self.positions.closed_positions.append(
                self.positions.active_positions)
            self.cash = self.cash + self.positions.active_positions.value
            self.positions.active_positions = None
        elif signals.signal_type == 2:
            # update price
            self.positions.active_positions.current_price = data.iloc[-1]['close']
        self.logger.debug('Cash %s', self.cash)

    def open_position(self, position):
        # TODO add short position logic
        self.logger.info('Open position: %s', position)
        self.positions.active_positions = position
        self.cash = self.cash - position.value

    @ property
    def portfolio_return(self):
        return (self.positions.total_value - self.strating_cash)/self.strating_cash

    @ property
    def total_portfolio_value(self):
        return self.cash + self.positions.total_value


class Position:
    def __init__(self, symbol, quantity, start_price):
        self.symbol = symbol
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = datetime.datetime.now()
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
