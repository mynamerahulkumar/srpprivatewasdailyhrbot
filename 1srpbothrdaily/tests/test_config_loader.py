"""Unit tests for configuration loader"""

import unittest
import tempfile
import os
from pathlib import Path
import yaml
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """Test cases for ConfigLoader"""
    
    def setUp(self):
        """Set up test configuration file"""
        self.test_config = {
            'trading': {
                'symbol': 'BTCUSD',
                'product_id': 27,
                'order_size': 1
            },
            'schedule': {
                'timeframe': '1h',
                'reset_interval_minutes': 60,
                'timezone': 'UTC'
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
            },
            'logging': {
                'level': 'INFO',
                'file': 'test.log'
            }
        }
        
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.yaml',
            delete=False
        )
        yaml.dump(self.test_config, self.temp_config)
        self.temp_config.close()
        
        # Create temporary .env file
        self.temp_env = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.env',
            delete=False,
            dir='.'
        )
        self.temp_env.write('DELTA_API_KEY=test_key\n')
        self.temp_env.write('DELTA_API_SECRET=test_secret\n')
        self.temp_env.close()
        
        # Rename to .env for testing
        if os.path.exists('.env.test'):
            os.remove('.env.test')
        os.rename(self.temp_env.name, '.env.test')
    
    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_config.name):
            os.remove(self.temp_config.name)
        if os.path.exists('.env.test'):
            os.remove('.env.test')
    
    def test_load_valid_config(self):
        """Test loading valid configuration"""
        # Set environment variables
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        
        self.assertEqual(loader.get('trading', 'symbol'), 'BTCUSD')
        self.assertEqual(loader.get('trading', 'product_id'), 27)
    
    def test_get_trading_config(self):
        """Test getting trading configuration"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        trading_config = loader.get_trading_config()
        
        self.assertEqual(trading_config['symbol'], 'BTCUSD')
        self.assertEqual(trading_config['product_id'], 27)
        self.assertEqual(trading_config['order_size'], 1)
    
    def test_get_risk_config(self):
        """Test getting risk management configuration"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        risk_config = loader.get_risk_config()
        
        self.assertEqual(risk_config['stop_loss_points'], 10000)
        self.assertEqual(risk_config['take_profit_points'], 40000)
        self.assertEqual(risk_config['breakeven_trigger_points'], 10000)
    
    def test_get_api_credentials(self):
        """Test getting API credentials"""
        os.environ['DELTA_API_KEY'] = 'my_test_key'
        os.environ['DELTA_API_SECRET'] = 'my_test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        api_key, api_secret = loader.get_api_credentials()
        
        self.assertEqual(api_key, 'my_test_key')
        self.assertEqual(api_secret, 'my_test_secret')
    
    def test_missing_config_file(self):
        """Test error handling for missing config file"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        with self.assertRaises(FileNotFoundError):
            ConfigLoader('nonexistent.yaml')
    
    @patch('src.config_loader.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_credentials(self, mock_load_dotenv):
        """Test error handling for missing API credentials"""
        # Mock load_dotenv to do nothing (not load any .env file)
        mock_load_dotenv.return_value = None
        
        # Ensure environment variables are not set
        with self.assertRaises(ValueError) as context:
            ConfigLoader(self.temp_config.name)
        
        self.assertIn('API credentials not found', str(context.exception))
    
    def test_missing_required_section(self):
        """Test validation of missing required section"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        # Create config without trading section
        invalid_config = {
            'schedule': {'reset_time': '00:00', 'timezone': 'UTC'},
            'risk_management': {'stop_loss_points': 10000, 'take_profit_points': 40000, 'breakeven_trigger_points': 10000},
            'monitoring': {'order_check_interval': 10, 'position_check_interval': 5},
            'api': {'base_url': 'https://api.test.delta.exchange'}
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(invalid_config, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(ValueError):
                ConfigLoader(temp_file.name)
        finally:
            os.remove(temp_file.name)
    
    def test_get_with_default(self):
        """Test getting config value with default"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        
        # Existing value
        value = loader.get('trading', 'symbol', 'DEFAULT')
        self.assertEqual(value, 'BTCUSD')
        
        # Non-existing value with default
        value = loader.get('trading', 'nonexistent', 'DEFAULT')
        self.assertEqual(value, 'DEFAULT')
    
    def test_logging_config_defaults(self):
        """Test logging configuration with defaults"""
        os.environ['DELTA_API_KEY'] = 'test_key'
        os.environ['DELTA_API_SECRET'] = 'test_secret'
        
        loader = ConfigLoader(self.temp_config.name)
        logging_config = loader.get_logging_config()
        
        self.assertEqual(logging_config['level'], 'INFO')
        self.assertEqual(logging_config['file'], 'test.log')


if __name__ == '__main__':
    unittest.main()

