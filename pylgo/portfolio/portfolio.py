import datetime


class Portfolio:
    def __init__(self, cash):
        self.strating_cash = cash
        self.cash = cash
        self.active_positions = []
        self.positions_value = 0

    def update(self, positions):
        for position in positions:
            self.active_positions.append(position)
            self.cash -= position.value
            # TODO better way of calculating value
        for active_position in self.active_positions:
            self.positions_value = active_position.value

    @ property
    def portfolio_return(self):
        return (self.positions_value - self.strating_cash)/self.strating_cash


class Position:
    def __init__(self, symbol, quantity, start_price):
        self.symbol = symbol
        self.quantity = quantity
        self.start_price = start_price
        self.current_price = start_price
        self.time = datetime.datetime.now()

    @property
    def value(self):
        return self.quantity * self.current_price
