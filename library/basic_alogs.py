from pylgo.algorithm import AlgorithmBase
from pylgo.alpha import Signal


class HODL(AlgorithmBase):
    # TODO here should data for indicators/models
    algo_name = 'HODL'

    def create_signals(self, data):
        if len(self.portfolio.active_positions) == 0:
            return [Signal(1)]
        return [Signal(0)]
