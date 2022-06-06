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
        self.update_positions_data(data_collection)
        number_buy_sell = sum((1 for signal in signals if signal.signal_type !=
                              0 or signal.signal_type != 2))
        target_pct = 1/number_buy_sell if number_buy_sell > 0 else 0
        # TODO add execution logic layer for scehduling signals
        signals.sort(key=lambda x: x.signal_type)
        for signal in signals:
            current_price = data_collection[signal.symbol].iloc[-1]['close']
            current_date = data_collection[signal.symbol].iloc[-1]['date']
            avialabe_qnty = target_pct*(self.cash / current_price)
            if signal.signal_type == 0:
                position = self.positions.get_position(signal.symbol)
                if position is not None:
                    self.close_position(position)
            elif signal.signal_type == 1:
                self.open_position(Position(
                    signal.symbol, avialabe_qnty, current_price, current_date))

    def open_position(self, position):
        # TODO add short position logic
        self.logger.info('Open position: %s', position)
        self.positions.add_position(position)
        self.cash = self.cash - position.value

    def close_position(self, position):
        self.logger.info('Close position: %s', position)
        self.positions.closed_positions.append(position)
        self.positions.remove_position(position)
        self.cash = self.cash + position.value

    # def update_position(self, position, price, qnty=None):
    #     # FIXME correct position access
    #     self.positions.active_positions.current_price = price

    def update_positions_data(self, current_data):
        for position in self.positions.active_positions:
            position.current_price = current_data[position.symbol].iloc[-1]['close']
            position.time = current_data[position.symbol].iloc[-1]['date']

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
        self.filled = False  # TODO finish it

    def __str__(self) -> str:
        return f'{self.time} {self.symbol}. Quantity {self.quantity} for a price {self.current_price}'

    @property
    def value(self):
        return self.quantity * self.current_price


class Positions:
    # TODO rewrite using named tuples.
    active_positions = []
    closed_positions = []
    logger = logging.getLogger('portfolio testing')

    def get_position(self, symbol):
        # TODO add cases when there are multiple postions for same symbol.
        for position in self.active_positions:
            if position.symbol == symbol:
                return position
        return None

    def remove_position(self, position):
        self.active_positions.remove(position)

    def add_position(self, position):
        # TODO add duplicate check
        self.active_positions.append(position)

    @ property
    def total_value(self):
        return sum(position.current_price * position.quantity for position in self.active_positions)

    @ property
    def active_positions_tickets(self):
        return [position.symbol for position in self.active_positions]
