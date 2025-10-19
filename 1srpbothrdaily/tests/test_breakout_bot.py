"""Integration tests for Breakout Trading Bot"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pytz

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.breakout_bot import BreakoutTradingBot
from src.delta_client import DeltaExchangeClient


class TestBreakoutTradingBot(unittest.TestCase):
    """Test cases for BreakoutTradingBot"""
    
    def setUp(self):
        """Set up test bot"""
        self.mock_client = Mock(spec=DeltaExchangeClient)
        
        self.bot = BreakoutTradingBot(
            client=self.mock_client,
            symbol='BTCUSD',
            product_id=27,
            order_size=1,
            stop_loss_points=10000,
            take_profit_points=40000,
            breakeven_trigger_points=10000,
            timeframe='1h',
            reset_interval_minutes=60,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
    
    def test_initialization(self):
        """Test bot initialization"""
        self.assertEqual(self.bot.symbol, 'BTCUSD')
        self.assertEqual(self.bot.product_id, 27)
        self.assertEqual(self.bot.order_size, 1)
        self.assertEqual(self.bot.stop_loss_points, 10000)
        self.assertEqual(self.bot.take_profit_points, 40000)
        self.assertEqual(self.bot.breakeven_trigger_points, 10000)
        self.assertEqual(self.bot.timeframe, '1h')
        self.assertEqual(self.bot.reset_interval_minutes, 60)
        self.assertIsNone(self.bot.prev_period_high)
        self.assertIsNone(self.bot.prev_period_low)
    
    def test_calculate_previous_period_levels_success(self):
        """Test successful calculation of previous period levels"""
        mock_candles = [
            {'time': 1000000, 'open': '58000', 'high': '62000', 'low': '57000', 'close': '60000'},
            {'time': 2000000, 'open': '60000', 'high': '65000', 'low': '59000', 'close': '63000'},
            {'time': 3000000, 'open': '63000', 'high': '64000', 'low': '61000', 'close': '62000'}
        ]
        
        self.mock_client.get_historical_candles.return_value = mock_candles
        
        high, low = self.bot.calculate_previous_period_levels()
        
        # Should get second-to-last candle
        self.assertEqual(high, 65000.0)
        self.assertEqual(low, 59000.0)
        self.mock_client.get_historical_candles.assert_called_once()
    
    def test_calculate_previous_period_levels_insufficient_data(self):
        """Test handling of insufficient candle data"""
        self.mock_client.get_historical_candles.return_value = [
            {'time': 1000000, 'open': '60000', 'high': '62000', 'low': '59000', 'close': '61000'}
        ]
        
        high, low = self.bot.calculate_previous_period_levels()
        
        self.assertIsNone(high)
        self.assertIsNone(low)
    
    def test_timeframe_to_minutes(self):
        """Test timeframe conversion to minutes"""
        test_cases = [
            ('1h', 60),
            ('2h', 120),
            ('4h', 240),
            ('1d', 1440),
            ('30m', 30)
        ]
        
        for timeframe, expected_minutes in test_cases:
            self.bot.timeframe = timeframe
            result = self.bot._timeframe_to_minutes()
            self.assertEqual(result, expected_minutes, f"Failed for {timeframe}")
    
    def test_place_breakout_orders_success(self):
        """Test successful placement of breakout orders"""
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Mock current price in range
        self.mock_client.get_ticker.return_value = {'close': '62000'}
        
        self.mock_client.place_limit_order.side_effect = [
            {'id': 101, 'side': 'buy', 'limit_price': '65000'},
            {'id': 102, 'side': 'sell', 'limit_price': '59000'}
        ]
        
        result = self.bot.place_breakout_orders()
        
        self.assertTrue(result)
        self.assertEqual(self.bot.buy_order_id, 101)
        self.assertEqual(self.bot.sell_order_id, 102)
        self.assertEqual(self.mock_client.place_limit_order.call_count, 2)
    
    def test_place_breakout_orders_no_levels(self):
        """Test order placement failure when levels not set"""
        self.bot.prev_period_high = None
        self.bot.prev_period_low = None
        
        result = self.bot.place_breakout_orders()
        
        self.assertFalse(result)
        self.mock_client.place_limit_order.assert_not_called()
    
    def test_check_order_status_buy_filled(self):
        """Test detection of filled buy order"""
        self.bot.buy_order_id = 101
        self.bot.sell_order_id = 102
        
        mock_position = {
            'product_id': 27,
            'size': '1',
            'entry_price': '65000'
        }
        
        self.mock_client.get_positions.return_value = [mock_position]
        
        result = self.bot.check_order_status()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.bot.active_position)
        self.assertEqual(self.bot.entry_price, 65000.0)
        self.assertEqual(self.bot.position_side, 'long')
        self.mock_client.cancel_order.assert_called_once_with(102, 27)
    
    def test_check_order_status_sell_filled(self):
        """Test detection of filled sell order"""
        self.bot.buy_order_id = 101
        self.bot.sell_order_id = 102
        
        mock_position = {
            'product_id': 27,
            'size': '-1',
            'entry_price': '59000'
        }
        
        self.mock_client.get_positions.return_value = [mock_position]
        
        result = self.bot.check_order_status()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.bot.active_position)
        self.assertEqual(self.bot.entry_price, 59000.0)
        self.assertEqual(self.bot.position_side, 'short')
        self.mock_client.cancel_order.assert_called_once_with(101, 27)
    
    def test_monitor_position_apply_breakeven_long(self):
        """Test breakeven logic for long position"""
        self.bot.active_position = {'product_id': 27, 'size': '1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'long'
        self.bot.stop_loss_order_id = 201
        self.bot.breakeven_applied = False
        
        # Current price is 70000 (10000 points profit)
        self.mock_client.get_ticker.return_value = {'close': '70000'}
        self.mock_client.edit_order.return_value = {'id': 201, 'stop_price': '60000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertTrue(self.bot.breakeven_applied)
        self.mock_client.edit_order.assert_called_once_with(
            order_id=201,
            product_id=27,
            stop_price='60000',
            limit_price='60000'
        )
    
    def test_monitor_position_apply_breakeven_short(self):
        """Test breakeven logic for short position"""
        self.bot.active_position = {'product_id': 27, 'size': '-1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'short'
        self.bot.stop_loss_order_id = 201
        self.bot.breakeven_applied = False
        
        # Current price is 50000 (10000 points profit)
        self.mock_client.get_ticker.return_value = {'close': '50000'}
        self.mock_client.edit_order.return_value = {'id': 201, 'stop_price': '60000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertTrue(self.bot.breakeven_applied)
        self.mock_client.edit_order.assert_called_once()
    
    def test_monitor_position_no_breakeven_trigger(self):
        """Test that breakeven is not applied when profit is insufficient"""
        self.bot.active_position = {'product_id': 27, 'size': '1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'long'
        self.bot.stop_loss_order_id = 201
        self.bot.breakeven_applied = False
        
        # Current price is 65000 (5000 points profit, below 10000 threshold)
        self.mock_client.get_ticker.return_value = {'close': '65000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertFalse(self.bot.breakeven_applied)
        self.mock_client.edit_order.assert_not_called()
    
    def test_check_position_closed(self):
        """Test detection of closed position"""
        self.bot.active_position = {'product_id': 27, 'size': '1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'long'
        
        # Position is now closed (size = 0)
        self.mock_client.get_positions.return_value = [
            {'product_id': 27, 'size': '0'}
        ]
        
        result = self.bot.check_position_closed()
        
        self.assertTrue(result)
        self.assertIsNone(self.bot.active_position)
        self.assertIsNone(self.bot.entry_price)
        self.assertIsNone(self.bot.position_side)
        self.assertFalse(self.bot.breakeven_applied)
    
    def test_should_reset_interval(self):
        """Test interval-based reset timing check"""
        # Set initial reset time
        self.bot.last_reset_time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        self.bot.reset_interval_minutes = 60
        self.bot.timezone = pytz.UTC
        
        with patch('src.breakout_bot.datetime') as mock_datetime:
            # Mock current time to be 61 minutes after last reset
            mock_now = datetime(2024, 1, 1, 1, 1, 0, tzinfo=pytz.UTC)
            mock_datetime.now.return_value = mock_now
            
            result = self.bot.should_reset()
            
            self.assertTrue(result)
    
    def test_should_reset_not_yet(self):
        """Test that reset doesn't trigger before interval passes"""
        # Set initial reset time
        self.bot.last_reset_time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        self.bot.reset_interval_minutes = 60
        self.bot.timezone = pytz.UTC
        
        with patch('src.breakout_bot.datetime') as mock_datetime:
            # Mock current time to be 30 minutes after last reset
            mock_now = datetime(2024, 1, 1, 0, 30, 0, tzinfo=pytz.UTC)
            mock_datetime.now.return_value = mock_now
            
            result = self.bot.should_reset()
            
            self.assertFalse(result)
    
    def test_perform_reset(self):
        """Test periodic reset procedure"""
        self.bot.buy_order_id = 101
        self.bot.sell_order_id = 102
        
        mock_candles = [
            {'time': 1000000, 'open': '60000', 'high': '65000', 'low': '59000', 'close': '63000'},
            {'time': 2000000, 'open': '63000', 'high': '67000', 'low': '62000', 'close': '66000'}
        ]
        
        self.mock_client.cancel_all_orders.return_value = True
        self.mock_client.get_historical_candles.return_value = mock_candles
        
        # Mock current price in range for new levels
        self.mock_client.get_ticker.return_value = {'close': '64000'}
        
        self.mock_client.place_limit_order.side_effect = [
            {'id': 201, 'side': 'buy'},
            {'id': 202, 'side': 'sell'}
        ]
        
        with patch('src.breakout_bot.datetime') as mock_datetime:
            mock_now = datetime(2024, 1, 1, 1, 0, 0, tzinfo=pytz.UTC)
            mock_datetime.now.return_value = mock_now
            
            self.bot.perform_reset()
        
        self.mock_client.cancel_all_orders.assert_called_once_with(product_id=27)
        self.assertIsNotNone(self.bot.buy_order_id)
        self.assertIsNotNone(self.bot.sell_order_id)
        self.assertEqual(self.bot.prev_period_high, 65000.0)
        self.assertEqual(self.bot.prev_period_low, 59000.0)
        self.assertIsNotNone(self.bot.last_reset_time)


class TestBreakoutBotEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test bot"""
        self.mock_client = Mock(spec=DeltaExchangeClient)
        
        self.bot = BreakoutTradingBot(
            client=self.mock_client,
            symbol='BTCUSD',
            product_id=27,
            order_size=1,
            stop_loss_points=10000,
            take_profit_points=40000,
            breakeven_trigger_points=10000,
            timeframe='1h',
            reset_interval_minutes=60,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
    
    def test_api_error_during_candle_fetch(self):
        """Test handling of API error during candle fetch"""
        self.mock_client.get_historical_candles.side_effect = Exception("API Error")
        
        high, low = self.bot.calculate_previous_period_levels()
        
        self.assertIsNone(high)
        self.assertIsNone(low)
    
    def test_order_placement_failure(self):
        """Test handling of order placement failure"""
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Mock current price in range
        self.mock_client.get_ticker.return_value = {'close': '62000'}
        
        # Buy order succeeds, sell order fails
        self.mock_client.place_limit_order.side_effect = [
            {'id': 101, 'side': 'buy'},
            {}  # Empty response indicates failure
        ]
        
        result = self.bot.place_breakout_orders()
        
        self.assertFalse(result)
        # Should cancel buy order on sell failure
        self.mock_client.cancel_order.assert_called_once()
    
    def test_breakeven_already_applied(self):
        """Test that breakeven is not applied twice"""
        self.bot.active_position = {'product_id': 27, 'size': '1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'long'
        self.bot.breakeven_applied = True  # Already applied
        
        self.mock_client.get_ticker.return_value = {'close': '70000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        # Should not call edit_order
        self.mock_client.edit_order.assert_not_called()
    
    def test_hourly_timeframe(self):
        """Test with 2-hour timeframe"""
        bot_2h = BreakoutTradingBot(
            client=self.mock_client,
            symbol='BTCUSD',
            product_id=27,
            order_size=1,
            stop_loss_points=10000,
            take_profit_points=40000,
            breakeven_trigger_points=10000,
            timeframe='2h',
            reset_interval_minutes=120,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
        
        self.assertEqual(bot_2h.timeframe, '2h')
        self.assertEqual(bot_2h.reset_interval_minutes, 120)
        self.assertEqual(bot_2h._timeframe_to_minutes(), 120)
    
    def test_4hour_timeframe(self):
        """Test with 4-hour timeframe"""
        bot_4h = BreakoutTradingBot(
            client=self.mock_client,
            symbol='BTCUSD',
            product_id=27,
            order_size=1,
            stop_loss_points=10000,
            take_profit_points=40000,
            breakeven_trigger_points=10000,
            timeframe='4h',
            reset_interval_minutes=240,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
        
        self.assertEqual(bot_4h.timeframe, '4h')
        self.assertEqual(bot_4h.reset_interval_minutes, 240)
        self.assertEqual(bot_4h._timeframe_to_minutes(), 240)


if __name__ == '__main__':
    unittest.main()
