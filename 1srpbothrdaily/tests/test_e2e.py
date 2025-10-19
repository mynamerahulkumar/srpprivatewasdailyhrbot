"""End-to-end tests for the Breakout Trading Bot"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
from datetime import datetime
import pytz

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.delta_client import DeltaExchangeClient
from src.breakout_bot import BreakoutTradingBot


class TestEndToEndScenario(unittest.TestCase):
    """End-to-end test scenarios"""
    
    def setUp(self):
        """Set up for E2E tests"""
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
            order_check_interval=1,  # Fast for testing
            position_check_interval=1
        )
    
    def test_complete_long_breakout_with_breakeven(self):
        """Test complete flow: setup -> breakout -> breakeven -> close"""
        
        # Step 1: Calculate previous period levels
        mock_candles = [
            {'time': 1000000, 'open': '58000', 'high': '62000', 'low': '57000', 'close': '60000'},
            {'time': 2000000, 'open': '60000', 'high': '65000', 'low': '59000', 'close': '63000'},
            {'time': 3000000, 'open': '63000', 'high': '64000', 'low': '61000', 'close': '62000'}
        ]
        self.mock_client.get_historical_candles.return_value = mock_candles
        
        high, low = self.bot.calculate_previous_period_levels()
        
        self.assertEqual(high, 65000.0)
        self.assertEqual(low, 59000.0)
        
        self.bot.prev_period_high = high
        self.bot.prev_period_low = low
        
        # Step 2: Place breakout orders
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
        
        # Step 3: Simulate buy order filled (long position opened)
        mock_position = {
            'product_id': 27,
            'size': '1',
            'entry_price': '65000'
        }
        self.mock_client.get_positions.return_value = [mock_position]
        
        # Reset mock for place_limit_order for SL/TP
        self.mock_client.place_limit_order.reset_mock()
        self.mock_client.place_limit_order.side_effect = [
            {'id': 201, 'side': 'sell', 'stop_price': '55000'},  # SL
            {'id': 202, 'side': 'sell', 'limit_price': '105000'}  # TP
        ]
        
        filled = self.bot.check_order_status()
        
        self.assertTrue(filled)
        self.assertEqual(self.bot.entry_price, 65000.0)
        self.assertEqual(self.bot.position_side, 'long')
        self.assertEqual(self.bot.stop_loss_order_id, 201)
        self.assertEqual(self.bot.take_profit_order_id, 202)
        
        # Step 4: Price moves to 75000 (10000 points profit) -> trigger breakeven
        self.mock_client.get_ticker.return_value = {'close': '75000'}
        self.mock_client.edit_order.return_value = {'id': 201, 'stop_price': '65000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertTrue(self.bot.breakeven_applied)
        
        # Step 5: Position closes at take profit
        self.mock_client.get_positions.return_value = [
            {'product_id': 27, 'size': '0'}
        ]
        
        closed = self.bot.check_position_closed()
        
        self.assertTrue(closed)
        self.assertIsNone(self.bot.active_position)
    
    def test_complete_short_breakout_with_breakeven(self):
        """Test complete flow for short position"""
        
        # Setup
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Place orders
        self.mock_client.place_limit_order.side_effect = [
            {'id': 101, 'side': 'buy', 'limit_price': '65000'},
            {'id': 102, 'side': 'sell', 'limit_price': '59000'}
        ]
        self.bot.place_breakout_orders()
        
        # Sell order filled (short position)
        mock_position = {
            'product_id': 27,
            'size': '-1',
            'entry_price': '59000'
        }
        self.mock_client.get_positions.return_value = [mock_position]
        
        # Reset and setup SL/TP placement
        self.mock_client.place_limit_order.reset_mock()
        self.mock_client.place_limit_order.side_effect = [
            {'id': 201, 'side': 'buy', 'stop_price': '69000'},  # SL
            {'id': 202, 'side': 'buy', 'limit_price': '19000'}  # TP
        ]
        
        self.bot.check_order_status()
        
        self.assertEqual(self.bot.position_side, 'short')
        
        # Price moves to 49000 (10000 points profit for short)
        self.mock_client.get_ticker.return_value = {'close': '49000'}
        self.mock_client.edit_order.return_value = {'id': 201}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertTrue(self.bot.breakeven_applied)
        
        # Position closes
        self.mock_client.get_positions.return_value = [{'product_id': 27, 'size': '0'}]
        self.bot.check_position_closed()
        
        self.assertIsNone(self.bot.active_position)
    
    def test_daily_reset_flow(self):
        """Test daily reset procedure"""
        
        # Setup initial state
        self.bot.buy_order_id = 101
        self.bot.sell_order_id = 102
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Mock for reset
        self.mock_client.cancel_all_orders.return_value = True
        
        new_candles = [
            {'time': 4000000, 'open': '62000', 'high': '68000', 'low': '61000', 'close': '67000'},
            {'time': 5000000, 'open': '67000', 'high': '70000', 'low': '66000', 'close': '69000'}
        ]
        self.mock_client.get_historical_candles.return_value = new_candles
        
        # Mock current price in range for new levels
        self.mock_client.get_ticker.return_value = {'close': '64000'}
        
        self.mock_client.place_limit_order.side_effect = [
            {'id': 201, 'side': 'buy', 'limit_price': '68000'},
            {'id': 202, 'side': 'sell', 'limit_price': '61000'}
        ]
        
        # Perform reset
        self.bot.perform_reset()
        
        # Verify state
        self.assertEqual(self.bot.prev_period_high, 68000.0)
        self.assertEqual(self.bot.prev_period_low, 61000.0)
        self.assertIsNotNone(self.bot.buy_order_id)
        self.assertIsNotNone(self.bot.sell_order_id)
        
        self.mock_client.cancel_all_orders.assert_called_once()
    
    def test_multiple_breakeven_attempts(self):
        """Test that breakeven is only applied once"""
        
        # Setup position
        self.bot.active_position = {'product_id': 27, 'size': '1'}
        self.bot.entry_price = 60000
        self.bot.position_side = 'long'
        self.bot.stop_loss_order_id = 201
        
        # First attempt: profit = 15000 points (above threshold)
        self.mock_client.get_ticker.return_value = {'close': '75000'}
        self.mock_client.edit_order.return_value = {'id': 201}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        self.assertTrue(self.bot.breakeven_applied)
        self.assertEqual(self.mock_client.edit_order.call_count, 1)
        
        # Second attempt: profit = 20000 points (even more profit)
        self.mock_client.get_ticker.return_value = {'close': '80000'}
        
        self.bot.monitor_position_and_apply_breakeven()
        
        # Should still be only 1 call (no additional edit)
        self.assertEqual(self.mock_client.edit_order.call_count, 1)
    
    def test_no_orders_when_levels_missing(self):
        """Test that orders are not placed without proper levels"""
        
        # No levels set
        self.bot.prev_period_high = None
        self.bot.prev_period_low = None
        
        result = self.bot.place_breakout_orders()
        
        self.assertFalse(result)
        self.mock_client.place_limit_order.assert_not_called()


class TestErrorRecovery(unittest.TestCase):
    """Test error recovery scenarios"""
    
    def setUp(self):
        """Set up for error recovery tests"""
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
            order_check_interval=1,
            position_check_interval=1
        )
    
    def test_recovery_from_api_timeout(self):
        """Test recovery from API timeout during order placement"""
        
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Mock current price in range
        self.mock_client.get_ticker.return_value = {'close': '62000'}
        
        # First attempt: timeout
        self.mock_client.place_limit_order.side_effect = Exception("Timeout")
        
        result = self.bot.place_breakout_orders()
        
        self.assertFalse(result)
        
        # Second attempt: success
        self.mock_client.place_limit_order.reset_mock()
        self.mock_client.place_limit_order.side_effect = [
            {'id': 101, 'side': 'buy'},
            {'id': 102, 'side': 'sell'}
        ]
        
        result = self.bot.place_breakout_orders()
        
        self.assertTrue(result)
    
    def test_handling_of_partial_position_data(self):
        """Test handling of incomplete position data"""
        
        self.bot.buy_order_id = 101
        
        # Position with missing fields
        incomplete_position = {
            'product_id': 27,
            'size': '1'
            # Missing entry_price
        }
        
        self.mock_client.get_positions.return_value = [incomplete_position]
        
        # Should handle gracefully
        try:
            self.bot.check_order_status()
            # If it reaches here without exception, test passes
            self.assertTrue(True)
        except KeyError:
            self.fail("Should handle missing position fields gracefully")


if __name__ == '__main__':
    unittest.main()

