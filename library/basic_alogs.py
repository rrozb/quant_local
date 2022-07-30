from pylgo.algorithm import AlgorithmBase
from pylgo.alpha import Signal, SignalType


class BuyLiquidateAlgo(AlgorithmBase):
    '''
    Test algo to just buy and then liquidate in the next step.
    '''
    algo_name = 'Buy Liquidate'

    def create_signals(self, current_data):
        for symbol, snapshot in current_data.items():
            symbol_data = snapshot.data
            if not symbol_data.empty:
                if len(self.portfolio.positions.active_positions) == 0:
                    yield Signal(SignalType.BUY, symbol)
                else:
                    yield Signal(SignalType.LIQUIDATE, symbol)


class SMAAlgo(AlgorithmBase):
    '''
    SMA Long/Short algorithm.
    '''
    algo_name = 'SMA'
    window_1 = 30
    window_2 = 100

    def create_signals(self, current_data):
        signals = []
        for symbol, snapshot in current_data.items():
            symbol_data = snapshot.data
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
                yield Signal(SignalType.BUY, symbol)
            elif symbol_position is None and not is_above:
                yield Signal(SignalType.SELL, symbol)

            if symbol_position is not None:
                position_type = symbol_position.signal.signal_type
                if position_type is SignalType.BUY and not is_above:
                    yield Signal(SignalType.LIQUIDATE, symbol)
                elif position_type is SignalType.SELL and is_above:
                    yield Signal(SignalType.LIQUIDATE, symbol)
        return signals
