from pylgo.algorithm import AlgorithmBase
from pylgo.alpha import Signal


class HODL(AlgorithmBase):
    # TODO here should data for indicators/models
    algo_name = 'HODL'

    def create_signals(self, data):
        # TODO refactor
        # TODO fix errors
        # TODO refactor after adding model
        first_elem = next(iter(data))
        data_one = data[first_elem]
        pass
        ###
        # if not data_one.empty:
        #     # for
        #     if self.portfolio.positions.active_positions is None:
        #         return Signal(1, self.symbol)
        #     return Signal(0, self.symbol)
