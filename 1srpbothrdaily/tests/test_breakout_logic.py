"""Test to verify breakout order logic is correct"""

import unittest
from unittest.mock import Mock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.breakout_bot import BreakoutTradingBot
from src.delta_client import DeltaExchangeClient


class TestBreakoutOrderLogic(unittest.TestCase):
    """Test that breakout orders are placed correctly"""
    
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
            timeframe='4h',
            reset_interval_minutes=240,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
    
    def test_breakout_order_types(self):
        """
        CRITICAL TEST: Verify breakout orders use STOP orders, not LIMIT
        
        Correct breakout logic:
        - Buy STOP-LIMIT above previous high (triggers on upside breakout)
        - Sell STOP-LIMIT below previous low (triggers on downside breakout)
        
        WRONG (current implementation):
        - Buy LIMIT at previous high (would execute if price falls TO high)
        - Sell LIMIT at previous low (would execute if price rises TO low)
        """
        self.bot.prev_period_high = 65000
        self.bot.prev_period_low = 59000
        
        # Mock current price in range
        self.mock_client.get_ticker.return_value = {'close': '62000'}
        
        self.mock_client.place_limit_order.side_effect = [
            {'id': 101, 'side': 'buy'},
            {'id': 102, 'side': 'sell'}
        ]
        
        self.bot.place_breakout_orders()
        
        # Check what orders were placed
        calls = self.mock_client.place_limit_order.call_args_list
        
        # First call should be BUY order
        buy_call = calls[0]
        buy_args = buy_call[1]  # keyword arguments
        
        print("\n" + "="*70)
        print("BREAKOUT ORDER ANALYSIS")
        print("="*70)
        print(f"\nPrevious 4H High: {self.bot.prev_period_high}")
        print(f"Previous 4H Low: {self.bot.prev_period_low}")
        print(f"\nBuy Order:")
        print(f"  Side: {buy_args['side']}")
        print(f"  Limit Price: {buy_args['limit_price']}")
        print(f"  Stop Price: {buy_args.get('stop_price', 'NOT SET - ERROR!')}")
        
        # Second call should be SELL order
        sell_call = calls[1]
        sell_args = sell_call[1]
        
        print(f"\nSell Order:")
        print(f"  Side: {sell_args['side']}")
        print(f"  Limit Price: {sell_args['limit_price']}")
        print(f"  Stop Price: {sell_args.get('stop_price', 'NOT SET - ERROR!')}")
        
        print("\n" + "="*70)
        print("EXPECTED BEHAVIOR FOR BREAKOUT TRADING:")
        print("="*70)
        print(f"\n✓ Buy STOP-LIMIT Order:")
        print(f"    Stop Price: {self.bot.prev_period_high} (or slightly above)")
        print(f"    Triggers when: Price RISES ABOVE {self.bot.prev_period_high}")
        print(f"    Result: LONG position on bullish breakout")
        
        print(f"\n✓ Sell STOP-LIMIT Order:")
        print(f"    Stop Price: {self.bot.prev_period_low} (or slightly below)")
        print(f"    Triggers when: Price FALLS BELOW {self.bot.prev_period_low}")
        print(f"    Result: SHORT position on bearish breakout")
        
        print("\n" + "="*70)
        print("CURRENT BEHAVIOR (WRONG!):")
        print("="*70)
        print(f"\n❌ Buy LIMIT Order at {self.bot.prev_period_high}:")
        print(f"    Executes when: Price is AT OR BELOW {self.bot.prev_period_high}")
        print(f"    Problem: This is NOT a breakout!")
        
        print(f"\n❌ Sell LIMIT Order at {self.bot.prev_period_low}:")
        print(f"    Executes when: Price is AT OR ABOVE {self.bot.prev_period_low}")
        print(f"    Problem: This is NOT a breakout!")
        print("\n" + "="*70)
        
        # The current implementation is WRONG
        # It should use stop_price for breakout orders
        if buy_args.get('stop_price') is None:
            self.fail("\n\n❌ CRITICAL ERROR: Buy order missing stop_price! This is NOT a breakout order!")
        
        if sell_args.get('stop_price') is None:
            self.fail("\n\n❌ CRITICAL ERROR: Sell order missing stop_price! This is NOT a breakout order!")


if __name__ == '__main__':
    unittest.main(verbosity=2)

