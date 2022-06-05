import datetime


class Signal:
    def __init__(self, signal_type, symbol) -> None:
        # TODO refactor with enum?
        self.signal_type = signal_type
        self.created_at = datetime.datetime.now()
        self.symbol = symbol
