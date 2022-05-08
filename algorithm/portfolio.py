class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.active_positions = []
        self.total_value = cash

    def add_position(self, position):
        self.active_positions.append(position)
        self.total_value += position.shares * position.price
        self.cash -= position.shares * position.price

    def remove_position(self, position):
        self.active_positions.remove(position)
        self.total_value -= position.shares * position.price
        self.cash += position.shares * position.price
