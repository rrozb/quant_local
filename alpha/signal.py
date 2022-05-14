import datetime


class Signal:
    def __init__(self, signal_type) -> None:
        # TODO add sympbol?
        # TODO refactor with enum?
        self.signal_type = signal_type
        self.created_at = datetime.datetime.now()
