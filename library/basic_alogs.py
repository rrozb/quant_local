from pylgo.algorithm import AlgorithmBase
from pylgo.alpha import Signal


class HODL(AlgorithmBase):
    # TODO here should data for indicators/models
    algo_name = 'HODL'

    def create_signals(self, data):
        # TODO refactor
        # TODO fix errors
        if not data.empty:
            if self.portfolio.positions.active_positions is None:
                return Signal(1, self.symbol)
            return Signal(0, self.symbol)
