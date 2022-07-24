import datetime
import logging


class Portfolio:
    def __init__(self, cash):
        self.strating_cash = cash
        self.cash = cash
        self.positions = Positions()
        self.logger = logging.getLogger('portfolio testing')
        self.initial_margin_requirement = 0.1
        self.blocked_cash = 0
        # TODO add margin calls
        # TODO add stop losses, trailing etc.
        # TODO add metadata - like old positions, cash, fees etc.

    def manage(self, signals, data_collection):
        self.update_positions_data(data_collection)
        number_buy_sell = sum((1 for signal in signals if signal.signal_type !=
                              0 or signal.signal_type != 2))
        # TODO add position sizing model
        target_pct = 1/number_buy_sell if number_buy_sell > 0 else 0
        position_cash = self.cash * target_pct
        # TODO add execution logic layer for scehduling signals
        signals.sort(key=lambda x: x.signal_type)
        for signal in signals:
            current_price = data_collection[signal.symbol].iloc[-1]['close']
            current_date = data_collection[signal.symbol].iloc[-1]['date']
            # TODO add correct rounding and making sure it is less than cash
            avialabe_qnty = (position_cash / current_price)
            if signal.signal_type == 0:
                position = self.positions.get_position(signal.symbol)
                if position is not None:
                    self.close_position(position)
            # TODO refactor after adding enums
            elif signal.signal_type > 0:
                self.open_position(Position(
                    signal.symbol, avialabe_qnty, current_price, signal.signal_type, current_date))

    def open_position(self, position):
        self.logger.info('Open position: %s', position)
        # buy
        if position.position_type == 1:
            self.cash = self.cash - position.value
        # Margin short
        else:
            # TODO refactor
            margin_required = (
                position.quantity*position.start_price)*self.initial_margin_requirement
            self.blocked_cash += margin_required
            self.cash = self.cash - margin_required
            position.margin = margin_required
        self.positions.add_position(position)

    def close_position(self, position):
        self.logger.info('Close position: %s', position)
        self.positions.closed_positions.append(position)
        self.positions.remove_position(position)
        if position.position_type == 1:
            self.cash = self.cash + position.value
        elif position.position_type == 2:
            self.blocked_cash -= position.margin
            self.cash += position.margin + position.value

    def update_positions_data(self, current_data):
        for position in self.positions.active_positions:
            position.current_price = current_data[position.symbol].iloc[-1]['close']
            position.time = current_data[position.symbol].iloc[-1]['date']

    @ property
    def total_portfolio_value(self):
        return self.cash + self.positions.total_value + self.blocked_cash

    @ property
    def portfolio_return(self):
        return (self.total_portfolio_value - self.strating_cash)/self.strating_cash


class Position:
    def __init__(self, symbol, quantity, start_price, position_type, time):
        self.symbol = symbol
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = time
        self.filled = False  # TODO finish it
        # Add enums BUY SELL
        self.position_type = position_type
        self.margin = 0

    def __str__(self) -> str:
        sign = '-' if self.position_type == 2 else ''
        return f'{self.time} {self.symbol}. Quantity {sign}{self.quantity} for a price {self.current_price}'

    @property
    def value(self):
        # TODO rename to current_value
        if self.position_type == 2:
            return (self.start_price * self.quantity) - (self.quantity * self.current_price)
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
        return sum(position.value for position in self.active_positions)

    @ property
    def active_positions_tickets(self):
        return [position.symbol for position in self.active_positions]
