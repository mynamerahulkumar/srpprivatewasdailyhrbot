"""Unit tests for Delta Exchange client"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.delta_client import DeltaExchangeClient


class TestDeltaExchangeClient(unittest.TestCase):
    """Test cases for DeltaExchangeClient"""
    
    def setUp(self):
        """Set up test client"""
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.base_url = "https://api.test.delta.exchange"
        
        self.client = DeltaExchangeClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url=self.base_url
        )
    
    def test_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.api_secret, self.api_secret)
        self.assertEqual(self.client.base_url, self.base_url)
        self.assertIsNotNone(self.client.session)
    
    def test_generate_signature(self):
        """Test signature generation"""
        message = "test_message"
        signature = self.client._generate_signature(message)
        
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)  # SHA256 hex is 64 chars
    
    def test_get_timestamp(self):
        """Test timestamp generation"""
        timestamp = self.client._get_timestamp()
        
        self.assertIsInstance(timestamp, str)
        self.assertTrue(timestamp.isdigit())
        self.assertGreater(int(timestamp), 1600000000)  # After Sept 2020
    
    def test_build_query_string_empty(self):
        """Test query string building with empty params"""
        query_string = self.client._build_query_string(None)
        self.assertEqual(query_string, '')
    
    def test_build_query_string_with_params(self):
        """Test query string building with parameters"""
        params = {'key1': 'value1', 'key2': 'value2'}
        query_string = self.client._build_query_string(params)
        
        self.assertTrue(query_string.startswith('?'))
        self.assertIn('key1=value1', query_string)
        self.assertIn('key2=value2', query_string)
    
    @patch('src.delta_client.requests.Session.get')
    def test_get_historical_candles_success(self, mock_get):
        """Test successful candle data retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': [
                {'open': '60000', 'high': '61000', 'low': '59000', 'close': '60500'},
                {'open': '60500', 'high': '62000', 'low': '60000', 'close': '61500'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        candles = self.client.get_historical_candles('BTCUSD', '1D', 1000000, 2000000)
        
        self.assertEqual(len(candles), 2)
        self.assertEqual(candles[0]['high'], '61000')
        mock_get.assert_called_once()
    
    @patch('src.delta_client.requests.Session.get')
    def test_get_ticker_success(self, mock_get):
        """Test successful ticker retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {
                'symbol': 'BTCUSD',
                'close': '60000',
                'volume': '1000'
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        ticker = self.client.get_ticker('BTCUSD')
        
        self.assertEqual(ticker['close'], '60000')
        self.assertEqual(ticker['symbol'], 'BTCUSD')
        mock_get.assert_called_once()
    
    @patch('src.delta_client.requests.Session.post')
    def test_place_limit_order_success(self, mock_post):
        """Test successful order placement"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {
                'id': 12345,
                'product_id': 27,
                'side': 'buy',
                'size': 1,
                'limit_price': '60000',
                'state': 'open'
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        order = self.client.place_limit_order(
            product_id=27,
            product_symbol='BTCUSD',
            side='buy',
            size=1,
            limit_price='60000'
        )
        
        self.assertEqual(order['id'], 12345)
        self.assertEqual(order['side'], 'buy')
        mock_post.assert_called_once()
    
    @patch('src.delta_client.requests.Session.put')
    def test_edit_order_success(self, mock_put):
        """Test successful order editing"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {
                'id': 12345,
                'limit_price': '61000',
                'state': 'open'
            }
        }
        mock_response.raise_for_status = Mock()
        mock_put.return_value = mock_response
        
        order = self.client.edit_order(
            order_id=12345,
            product_id=27,
            limit_price='61000'
        )
        
        self.assertEqual(order['id'], 12345)
        self.assertEqual(order['limit_price'], '61000')
        mock_put.assert_called_once()
    
    @patch('src.delta_client.requests.Session.get')
    def test_get_open_orders_success(self, mock_get):
        """Test successful open orders retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': [
                {'id': 1, 'state': 'open', 'side': 'buy'},
                {'id': 2, 'state': 'open', 'side': 'sell'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        orders = self.client.get_open_orders(product_id=27)
        
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]['state'], 'open')
        mock_get.assert_called_once()
    
    @patch('src.delta_client.requests.Session.get')
    def test_get_positions_success(self, mock_get):
        """Test successful positions retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': [
                {'product_id': 27, 'size': '1', 'entry_price': '60000'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        positions = self.client.get_positions(product_id=27)
        
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0]['product_id'], 27)
        mock_get.assert_called_once()
    
    @patch('src.delta_client.requests.Session.delete')
    def test_cancel_order_success(self, mock_delete):
        """Test successful order cancellation"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {'id': 12345}
        }
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        result = self.client.cancel_order(order_id=12345, product_id=27)
        
        self.assertTrue(result)
        mock_delete.assert_called_once()
    
    @patch('src.delta_client.requests.Session.delete')
    def test_cancel_all_orders_success(self, mock_delete):
        """Test successful cancellation of all orders"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True
        }
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        result = self.client.cancel_all_orders(product_id=27)
        
        self.assertTrue(result)
        mock_delete.assert_called_once()
    
    @patch('src.delta_client.requests.Session.get')
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'error': {'code': 'invalid_request', 'message': 'Invalid parameters'}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        ticker = self.client.get_ticker('INVALID')
        
        self.assertEqual(ticker, {})


class TestDeltaClientIntegration(unittest.TestCase):
    """Integration tests for Delta client (requires mocking or testnet)"""
    
    def setUp(self):
        """Set up for integration tests"""
        self.api_key = "test_key"
        self.api_secret = "test_secret"
        self.base_url = "https://api.test.delta.exchange"
        
        self.client = DeltaExchangeClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url=self.base_url
        )
    
    def test_signature_consistency(self):
        """Test that signature generation is consistent"""
        message = "GET1234567890/v2/ticker"
        
        sig1 = self.client._generate_signature(message)
        sig2 = self.client._generate_signature(message)
        
        self.assertEqual(sig1, sig2)
    
    def test_signature_uniqueness(self):
        """Test that different messages produce different signatures"""
        message1 = "GET1234567890/v2/ticker"
        message2 = "POST1234567890/v2/orders"
        
        sig1 = self.client._generate_signature(message1)
        sig2 = self.client._generate_signature(message2)
        
        self.assertNotEqual(sig1, sig2)


if __name__ == '__main__':
    unittest.main()

