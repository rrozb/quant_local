from pylgo.algorithm import AlgorithmBase
from pylgo.alpha import Signal


class HODL(AlgorithmBase):
    # TODO here should data for indicators/models
    algo_name = 'HODL'

    def create_signals(self, current_data):
        signals = []
        for symbol, symbol_data in current_data.items():
            # TODO move empty check to base - create signals should't be called if no data.
            if not symbol_data.empty:
                if self.portfolio.positions.active_positions is None:
                    signals.append(Signal(1, symbol))
                else:
                    signals.append(Signal(0, symbol))
        return signals
