from typing import List
import logging
import pandas as pd
from ..alpha import Signal, SignalType
from .positions import Position, Positions


class Portfolio:
    '''
    Portfolio managment. Opening and closing new positions based on provided signals.
    '''

    def __init__(self, cash: int, stop_loss: float = None, take_profit: float = None):
        self.strating_cash = cash
        self.cash = cash
        self.positions = Positions()
        self.logger = logging.getLogger('portfolio testing')
        self.initial_margin_requirement = 0.1
        self.blocked_cash = 0
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.fees = 0.0

    def manage(self, signals: List[Signal], data_collection: pd.DataFrame):
        '''
        Create or close positions.
        '''
        self.update_positions_data(data_collection)
        self.validate_positions()
        number_buy_sell = sum((1 for signal in signals if signal.signal_type !=
                              0 or signal.signal_type != 2))
        target_pct = 1/number_buy_sell if number_buy_sell > 0 else 0
        position_cash = self.cash * target_pct
        for signal in signals:
            current_price = data_collection[signal.symbol].get_value(
                'close', -1)
            current_date = data_collection[signal.symbol].get_value(
                'date', -1)
            avialabe_qnty = (position_cash / current_price)
            position_stop_loss = self.stop_loss if signal.stop_loss is None else signal.stop_loss
            position_take_profit = self.take_profit if signal.take_profit is None else signal.take_profit
            if signal.signal_type is SignalType.LIQUIDATE:
                position = self.positions.get_position(signal.symbol)
                if position is not None:
                    self.close_position(position)
            else:
                self.open_position(Position(
                    signal, avialabe_qnty, current_price, current_date, position_stop_loss, position_take_profit))

    def open_position(self, position: Position):
        '''
        Open a new position.
        '''
        self.logger.info('Open position: %s', position)
        # buy
        if position.signal.signal_type is SignalType.BUY:
            self.cash = self.cash - position.quantity * \
                position.start_price*(1+self.fees)
        # Margin short
        else:
            # TODO add interest rate and check if this fee is correct.
            margin_required = (
                position.quantity*position.start_price)*self.initial_margin_requirement
            self.blocked_cash += margin_required*(1+self.fees)
            self.cash = self.cash - margin_required*(1+self.fees)
            position.margin = margin_required
        self.positions.add_position(position)

    def close_position(self, position, stop_hit=False):
        '''
        Close existing position.
        '''
        stop_message = ' stop loss was hit' if stop_hit else ''
        self.logger.info(
            f'Close position {stop_message}: %s, net profit {position.profit}', position)
        self.positions.remove_position(position)
        if position.signal.signal_type is SignalType.BUY:
            self.cash = self.cash + position.current_value*(1-self.fees)
        elif position.signal.signal_type is SignalType.SELL:
            self.blocked_cash -= position.margin
            self.cash += position.margin + position.current_value*(1-self.fees)

    def update_positions_data(self, current_data):
        '''
        Pass current price to open positions.
        '''
        for position in self.positions.active_positions:
            position.current_price = current_data[position.signal.symbol].get_value(
                'close', -1)
            position.time = current_data[position.signal.symbol].get_value(
                'date', -1)

    def validate_positions(self):
        """
        Validate positions.
        """
        for position in self.positions.active_positions:
            if position.stop_loss_hit or position.take_profit_hit:
                self.close_position(position, stop_hit=True)

    @ property
    def total_portfolio_value(self):
        '''
        Calculate total portfolio value.
        '''
        return self.cash + self.positions.total_value + self.blocked_cash

    @ property
    def portfolio_return(self):
        '''
        Calculate total portfolio return.
        '''
        return (self.total_portfolio_value - self.strating_cash)/self.strating_cash
