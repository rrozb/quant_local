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
                if len(self.portfolio.positions.active_positions) == 0:
                    signals.append(Signal(1, symbol))
                else:
                    signals.append(Signal(0, symbol))
        return signals


class SMAAlgo(AlgorithmBase):
    algo_name = 'SMA'
    window_1 = 30
    window_2 = 100

    def create_signals(self, current_data):
        signals = []
        for symbol, symbol_data in current_data.items():
            if len(symbol_data) < self.window_2:
                continue
            sma_30 = symbol_data['close'].rolling(
                self.window_1).mean().iloc[-1]
            sma_100 = symbol_data['close'].rolling(
                self.window_2).mean().iloc[-1]
            is_above = sma_30 > sma_100
            symbol_position = self.portfolio.positions.get_symbol_position(
                symbol)
            if symbol_position is None and is_above:
                signals.append(Signal(1, symbol))
            elif symbol_position is None and not is_above:
                signals.append(Signal(2, symbol))

            if symbol_position is not None:
                position_type = symbol_position.position_type
                if position_type == 1 and not is_above:
                    signals.append(Signal(0, symbol))
                elif position_type == 2 and is_above:
                    signals.append(Signal(0, symbol))
        return signals
