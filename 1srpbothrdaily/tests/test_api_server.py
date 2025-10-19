"""Tests for FastAPI server"""

import unittest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from api_server import app


class TestAPIServer(unittest.TestCase):
    """Test API server endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
        
        self.test_config = {
            "bot_id": "test_bot_1",
            "api_key": "test_key",
            "api_secret": "test_secret",
            "trading": {
                "symbol": "BTCUSD",
                "product_id": 27,
                "order_size": 1
            },
            "schedule": {
                "timeframe": "4h",
                "timezone": "Asia/Kolkata",
                "wait_for_next_candle": True,
                "startup_delay_minutes": 5
            },
            "risk_management": {
                "stop_loss_points": 10000,
                "take_profit_points": 40000,
                "breakeven_trigger_points": 10000
            },
            "monitoring": {
                "order_check_interval": 10,
                "position_check_interval": 5
            }
        }
    
    def test_health_check(self):
        """Test API health check endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'online')
        self.assertIn('version', data)
        print("✓ Health check works")
    
    def test_start_bot_invalid_timeframe(self):
        """Test starting bot with invalid timeframe"""
        invalid_config = self.test_config.copy()
        invalid_config['schedule']['timeframe'] = '5h'  # Invalid
        
        response = self.client.post("/api/v1/bot/start", json=invalid_config)
        self.assertEqual(response.status_code, 422)  # Validation error
        print("✓ Invalid timeframe rejected")
    
    def test_get_nonexistent_bot(self):
        """Test getting status of non-existent bot"""
        response = self.client.get("/api/v1/bot/status/nonexistent")
        self.assertEqual(response.status_code, 404)
        print("✓ Non-existent bot returns 404")
    
    def test_list_bots_empty(self):
        """Test listing bots when none exist"""
        response = self.client.get("/api/v1/bots")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("✓ List bots returns empty list")
    
    def test_stop_nonexistent_bot(self):
        """Test stopping non-existent bot"""
        response = self.client.post("/api/v1/bot/stop/nonexistent")
        self.assertEqual(response.status_code, 404)
        print("✓ Cannot stop non-existent bot")
    
    def test_delete_nonexistent_bot(self):
        """Test deleting non-existent bot"""
        response = self.client.delete("/api/v1/bot/nonexistent")
        self.assertEqual(response.status_code, 404)
        print("✓ Cannot delete non-existent bot")
    
    def test_validation_missing_fields(self):
        """Test validation for missing required fields"""
        incomplete_config = {
            "bot_id": "test",
            "api_key": "key"
            # Missing many required fields
        }
        
        response = self.client.post("/api/v1/bot/start", json=incomplete_config)
        self.assertEqual(response.status_code, 422)
        print("✓ Missing fields rejected")
    
    def test_validation_negative_values(self):
        """Test validation for negative values"""
        invalid_config = self.test_config.copy()
        invalid_config['risk_management']['stop_loss_points'] = -1000
        
        response = self.client.post("/api/v1/bot/start", json=invalid_config)
        self.assertEqual(response.status_code, 422)
        print("✓ Negative values rejected")


class TestAPIEndpointStructure(unittest.TestCase):
    """Test API endpoint structure and responses"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_docs_available(self):
        """Test that API documentation is available"""
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        print("✓ Swagger docs available")
    
    def test_openapi_schema(self):
        """Test that OpenAPI schema is available"""
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertIn('paths', schema)
        self.assertIn('info', schema)
        print("✓ OpenAPI schema valid")


if __name__ == '__main__':
    unittest.main(verbosity=2)



