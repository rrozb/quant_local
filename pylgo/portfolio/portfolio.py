import datetime


class Portfolio:
    def __init__(self, cash):
        self.strating_cash = cash
        self.cash = cash
        self.positions = Positions()

    def manage(self, signals, data):
        net_transaction = self.positions.update(signals, data)
        # for position in positions:
        #     self.positions.active_positions.append(position)
        #     self.cash -= position.value
        # TODO add positions
        # TODO calculate cash

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

    @property
    def value(self):
        return self.quantity * self.current_price


class Positions:
    # TODO rewrite using named tuples.
    active_positions = None
    closed_positions = []

    @ property
    def total_value(self):
        return self.active_positions.current_price
        # return sum([position.current_price for position in self.active_positions])

    @ property
    def active_positions_tickets(self):
        return self.active_positions.symbol
        # return [position.symbol for position in self.active_positions]

    def update(self, signals, data):
        # TODO more generic rather than just close.
        # TODO access value directly.
        if self.active_positions is not None:
            self.active_positions.current_price = float(data.iloc[-1]['close'])

        if signals.signal_type == 1:
            if self.active_positions is None:
                self.active_positions = Position(
                    signals.symbol, signals.quantity, float(data.iloc[-1]['close']))

    def update_prices(self):
        pass
