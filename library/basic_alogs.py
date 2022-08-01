from ta.volatility import BollingerBands
from ta.trend import MACD
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


class BBAlgo(AlgorithmBase):
    '''
    Boilinger bandas Long/Short algorithm.
    '''
    algo_name = 'BB'
    window = 30
    deviation = 2.5

    def create_signals(self, current_data):
        signals = []
        for symbol, snapshot in current_data.items():
            symbol_data = snapshot.data
            if len(symbol_data) < self.window:
                continue
            indicator_bb = BollingerBands(
                close=symbol_data["close"], window=self.window, window_dev=self.deviation)
            symbol_data = symbol_data.copy()
            # Add Bollinger Bands features
            symbol_data['bb_bbm'] = list(indicator_bb.bollinger_mavg().values)
            symbol_data['bb_bbh'] = list(indicator_bb.bollinger_hband().values)
            symbol_data['bb_bbl'] = list(indicator_bb.bollinger_lband().values)

            # Add Bollinger Band high indicator
            symbol_data['bb_bbhi'] = list(
                indicator_bb.bollinger_hband_indicator().values)

            # Add Bollinger Band low indicator
            symbol_data['bb_bbli'] = list(
                indicator_bb.bollinger_lband_indicator().values)
            symbol_position = self.portfolio.positions.get_symbol_position(
                symbol)
            is_buy = symbol_data['bb_bbli'].iloc[-1] == 1
            is_sell = symbol_data['bb_bbhi'].iloc[-1] == 1
            if symbol_position is None and is_buy:
                yield Signal(SignalType.BUY, symbol)
            elif symbol_position is None and not is_sell:
                yield Signal(SignalType.SELL, symbol)

            if symbol_position is not None:
                position_type = symbol_position.signal.signal_type
                below_mavg = symbol_data['close'].iloc[-1] <= symbol_data['bb_bbm'].iloc[-1]
                above_mavg = symbol_data['close'].iloc[-1] >= symbol_data['bb_bbm'].iloc[-1]
                if position_type is SignalType.BUY and not above_mavg:
                    yield Signal(SignalType.LIQUIDATE, symbol)
                elif position_type is SignalType.SELL and below_mavg:
                    yield Signal(SignalType.LIQUIDATE, symbol)

        return signals


class MACDAlgo(AlgorithmBase):
    '''
    MACDAlgo bandas Long/Short algorithm.
    '''
    algo_name = 'MACD'
    window_slow: int = 26
    window_fast: int = 12
    window_sign: int = 9

    def create_signals(self, current_data):
        signals = []
        for symbol, snapshot in current_data.items():
            symbol_data = snapshot.data
            if len(symbol_data) < self.window_slow:
                continue

            indicator_macd = MACD(
                close=symbol_data["close"], window_slow=self.window_slow,
                window_fast=self.window_fast, window_sign=self.window_sign
            )
            symbol_data = symbol_data.copy()
            # Add MACD features
            symbol_data['macd'] = indicator_macd.macd()
            symbol_data['macd_diff'] = indicator_macd.macd_diff()
            symbol_data['macd_signal'] = indicator_macd.macd_signal()
            symbol_position = self.portfolio.positions.get_symbol_position(
                symbol)
            is_buy = symbol_data['macd_diff'].iloc[-1] < 0
            is_sell = symbol_data['macd_diff'].iloc[-1] >= 0
            if symbol_position is None and is_buy:
                yield Signal(SignalType.BUY, symbol)
            elif symbol_position is None and not is_sell:
                yield Signal(SignalType.SELL, symbol)

            if symbol_position is not None:
                position_type = symbol_position.signal.signal_type
                if position_type is SignalType.BUY and is_buy:
                    yield Signal(SignalType.LIQUIDATE, symbol)
                    yield Signal(SignalType.SELL, symbol)
                elif position_type is SignalType.SELL and is_sell:
                    yield Signal(SignalType.LIQUIDATE, symbol)
                    yield Signal(SignalType.BUY, symbol)

        return signals
