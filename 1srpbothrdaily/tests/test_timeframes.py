"""Test different timeframe configurations"""

import unittest
import tempfile
import os
import yaml
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import ConfigLoader
from src.breakout_bot import BreakoutTradingBot
from src.delta_client import DeltaExchangeClient


class TestTimeframeConfigurations(unittest.TestCase):
    """Test various timeframe configurations"""
    
    def setUp(self):
        """Set up test environment"""
        # Set environment variables
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
    
    def create_config_with_timeframe(self, timeframe: str):
        """Helper to create a config file with specific timeframe"""
        config = {
            'trading': {
                'symbol': 'BTCUSD',
                'product_id': 27,
                'order_size': 1
            },
            'schedule': {
                'timeframe': timeframe,
                'timezone': 'UTC'
                # Note: reset_interval_minutes is auto-calculated
            },
            'risk_management': {
                'stop_loss_points': 10000,
                'take_profit_points': 40000,
                'breakeven_trigger_points': 10000
            },
            'monitoring': {
                'order_check_interval': 10,
                'position_check_interval': 5
            },
            'api': {
                'base_url': 'https://api.test.delta.exchange'
            }
        }
        
        temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.yaml',
            delete=False
        )
        yaml.dump(config, temp_config)
        temp_config.close()
        
        return temp_config.name
    
    def test_30min_timeframe(self):
        """Test 30-minute breakout configuration"""
        config_path = self.create_config_with_timeframe('30m')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '30m')
            self.assertEqual(schedule_config['reset_interval_minutes'], 30)
            print("✓ 30-minute timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_1hour_timeframe(self):
        """Test 1-hour breakout configuration"""
        config_path = self.create_config_with_timeframe('1h')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '1h')
            self.assertEqual(schedule_config['reset_interval_minutes'], 60)
            print("✓ 1-hour timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_2hour_timeframe(self):
        """Test 2-hour breakout configuration"""
        config_path = self.create_config_with_timeframe('2h')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '2h')
            self.assertEqual(schedule_config['reset_interval_minutes'], 120)
            print("✓ 2-hour timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_4hour_timeframe(self):
        """Test 4-hour breakout configuration"""
        config_path = self.create_config_with_timeframe('4h')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '4h')
            self.assertEqual(schedule_config['reset_interval_minutes'], 240)
            print("✓ 4-hour timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_6hour_timeframe(self):
        """Test 6-hour breakout configuration"""
        config_path = self.create_config_with_timeframe('6h')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '6h')
            self.assertEqual(schedule_config['reset_interval_minutes'], 360)
            print("✓ 6-hour timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_daily_timeframe(self):
        """Test daily breakout configuration"""
        config_path = self.create_config_with_timeframe('1d')
        
        try:
            loader = ConfigLoader(config_path)
            schedule_config = loader.get_schedule_config()
            
            self.assertEqual(schedule_config['timeframe'], '1d')
            self.assertEqual(schedule_config['reset_interval_minutes'], 1440)
            print("✓ Daily timeframe configured successfully")
            
        finally:
            os.remove(config_path)
    
    def test_invalid_timeframe(self):
        """Test that invalid timeframe raises error"""
        config_path = self.create_config_with_timeframe('5h')  # Invalid
        
        try:
            with self.assertRaises(ValueError) as context:
                loader = ConfigLoader(config_path)
            
            self.assertIn('Invalid timeframe', str(context.exception))
            print("✓ Invalid timeframe properly rejected")
            
        finally:
            os.remove(config_path)
    
    def test_all_supported_timeframes(self):
        """Test all supported timeframes"""
        timeframes = {
            '1m': 1,
            '3m': 3,
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60,
            '2h': 120,
            '4h': 240,
            '6h': 360,
            '1d': 1440,
            '1w': 10080
        }
        
        for timeframe, expected_minutes in timeframes.items():
            config_path = self.create_config_with_timeframe(timeframe)
            
            try:
                loader = ConfigLoader(config_path)
                schedule_config = loader.get_schedule_config()
                
                self.assertEqual(schedule_config['timeframe'], timeframe)
                self.assertEqual(schedule_config['reset_interval_minutes'], expected_minutes)
                
            finally:
                os.remove(config_path)
        
        print(f"✓ All {len(timeframes)} timeframes tested successfully")


class TestTimeframeBotIntegration(unittest.TestCase):
    """Test bot with different timeframe configurations"""
    
    def setUp(self):
        """Set up mock client"""
        self.mock_client = Mock(spec=DeltaExchangeClient)
    
    def test_bot_with_30min_timeframe(self):
        """Test bot initialization with 30-minute timeframe"""
        bot = BreakoutTradingBot(
            client=self.mock_client,
            symbol='BTCUSD',
            product_id=27,
            order_size=1,
            stop_loss_points=10000,
            take_profit_points=40000,
            breakeven_trigger_points=10000,
            timeframe='30m',
            reset_interval_minutes=30,
            timezone='UTC',
            order_check_interval=10,
            position_check_interval=5
        )
        
        self.assertEqual(bot.timeframe, '30m')
        self.assertEqual(bot.reset_interval_minutes, 30)
        self.assertEqual(bot._timeframe_to_minutes(), 30)
        print("✓ Bot works with 30-minute timeframe")
    
    def test_bot_with_2hour_timeframe(self):
        """Test bot initialization with 2-hour timeframe"""
        bot = BreakoutTradingBot(
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
        
        self.assertEqual(bot.timeframe, '2h')
        self.assertEqual(bot.reset_interval_minutes, 120)
        self.assertEqual(bot._timeframe_to_minutes(), 120)
        print("✓ Bot works with 2-hour timeframe")
    
    def test_bot_with_4hour_timeframe(self):
        """Test bot initialization with 4-hour timeframe"""
        bot = BreakoutTradingBot(
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
        
        self.assertEqual(bot.timeframe, '4h')
        self.assertEqual(bot.reset_interval_minutes, 240)
        self.assertEqual(bot._timeframe_to_minutes(), 240)
        print("✓ Bot works with 4-hour timeframe")
    
    def test_calculate_levels_with_different_timeframes(self):
        """Test calculating previous period levels with different timeframes"""
        timeframe_intervals = {
            '30m': 30,
            '1h': 60,
            '2h': 120,
            '4h': 240,
            '1d': 1440
        }
        
        for timeframe, interval in timeframe_intervals.items():
            bot = BreakoutTradingBot(
                client=self.mock_client,
                symbol='BTCUSD',
                product_id=27,
                order_size=1,
                stop_loss_points=10000,
                take_profit_points=40000,
                breakeven_trigger_points=10000,
                timeframe=timeframe,
                reset_interval_minutes=interval,
                timezone='UTC',
                order_check_interval=10,
                position_check_interval=5
            )
            
            # Mock candle data
            mock_candles = [
                {'time': 1000000, 'open': '58000', 'high': '62000', 'low': '57000', 'close': '60000'},
                {'time': 2000000, 'open': '60000', 'high': '65000', 'low': '59000', 'close': '63000'},
                {'time': 3000000, 'open': '63000', 'high': '64000', 'low': '61000', 'close': '62000'}
            ]
            self.mock_client.get_historical_candles.return_value = mock_candles
            
            high, low = bot.calculate_previous_period_levels()
            
            self.assertEqual(high, 65000.0)
            self.assertEqual(low, 59000.0)
            
            # Verify correct resolution was requested
            call_args = self.mock_client.get_historical_candles.call_args
            self.assertEqual(call_args[1]['resolution'], timeframe)
        
        print(f"✓ Tested period level calculation for {len(timeframe_intervals)} timeframes")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

