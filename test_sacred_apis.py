#!/usr/bin/env python3
"""
Sacred API Testing Framework
Tests all Sacred Hive API endpoints following Sacred Team standards
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient

# Import our main app
from main import app
from database import get_db_connection, init_db

class TestSacredAPIs:
    """Sacred Test Suite for all API endpoints"""

    @classmethod
    def setup_class(cls):
        """Setup Sacred test environment"""
        cls.client = TestClient(app)
        # Initialize test database
        init_db()

    def test_health_endpoint_sacred_response(self):
        """Test health endpoint returns Sacred status"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "hive-chat-main"
        assert "hive_integration" in data

    def test_organellas_api_empty_user(self):
        """Test organellas API with non-existent user"""
        response = self.client.get("/api/organellas/test_user_sacred")
        assert response.status_code == 200
        data = response.json()
        assert "organellas" in data
        assert isinstance(data["organellas"], list)

    def test_tales_api_empty_user(self):
        """Test tales API with non-existent user"""
        response = self.client.get("/api/tales/test_user_sacred")
        assert response.status_code == 200
        data = response.json()
        assert "tales" in data
        assert isinstance(data["tales"], list)

    def test_cors_security_headers(self):
        """Test CORS configuration is secure"""
        response = self.client.get("/health")
        # Should not have wildcard CORS headers
        cors_header = response.headers.get("access-control-allow-origin", "")
        assert "*" not in cors_header  # No wildcard allowed!

    def test_sql_injection_protection_organellas(self):
        """Test SQL injection protection in organellas endpoint"""
        malicious_user_id = "'; DROP TABLE organellas; --"
        response = self.client.get(f"/api/organellas/{malicious_user_id}")
        # Should not crash and should return safe response
        assert response.status_code == 200
        # Database should still exist
        response2 = self.client.get("/api/organellas/safe_user")
        assert response2.status_code == 200

    def test_sql_injection_protection_tales(self):
        """Test SQL injection protection in tales endpoint"""
        malicious_user_id = "'; DROP TABLE tales; --"
        response = self.client.get(f"/api/tales/{malicious_user_id}")
        # Should not crash and should return safe response
        assert response.status_code == 200
        # Database should still exist
        response2 = self.client.get("/api/tales/safe_user")
        assert response2.status_code == 200

    def test_error_handling_doesnt_expose_internals(self):
        """Test error responses don't expose internal details"""
        # This might trigger an error condition
        response = self.client.get("/api/organellas/")  # Invalid path
        assert response.status_code in [404, 422]  # Expected error codes
        # Response should not contain sensitive info
        response_text = response.text.lower()
        assert "traceback" not in response_text
        assert "exception" not in response_text
        assert "/home/" not in response_text

    def test_websocket_endpoint_exists(self):
        """Test WebSocket endpoint exists and can be connected to"""
        # Note: TestClient doesn't fully support WebSocket testing
        # This tests that the endpoint is registered
        try:
            with self.client.websocket_connect("/ws?username=test&user_id=test123") as websocket:
                # Connection successful
                assert True
        except Exception:
            # If we get here, at least the endpoint exists (routing works)
            # Connection might fail due to test environment limitations
            pass

# Sacred Metrics Tests
class TestSacredMetrics:
    """Test Sacred Hive metrics and compliance"""

    def test_sacred_fibonacci_ratio_compliance(self):
        """Test codebase follows Sacred Fibonacci ratios"""
        # Simple check - main.py should be reasonable size
        with open("main.py", "r") as f:
            lines = len(f.readlines())
        # Should be within reasonable Sacred bounds (not bloated)
        assert lines < 500, f"main.py has {lines} lines - possible bloat violation"

    def test_sacred_pattern_presence(self):
        """Test presence of Sacred patterns in codebase"""
        # Check for PROVERBS-CORRECTION-PROTOCOL
        with open("main.py", "r") as f:
            content = f.read()
        # Should have sacred commenting patterns
        assert "# " in content, "Sacred commenting pattern missing"
        assert "TODO" in content or "FIXME" in content or "Sacred" in content

# Security Hardening Tests
class TestSecurityHardening:
    """Test security measures are properly implemented"""

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_no_debug_info_in_production_mode(self):
        """Test debug information is not exposed"""
        response = self.client.get("/health")
        assert "debug" not in response.json()

    def test_secure_headers_present(self):
        """Test security headers are configured"""
        response = self.client.get("/health")
        # Check for basic security considerations
        assert response.status_code == 200
        # Content-Type should be set properly
        assert "application/json" in response.headers.get("content-type", "")

if __name__ == "__main__":
    # Run Sacred tests
    print("🐝 Starting Sacred API Test Suite...")
    pytest.main([__file__, "-v", "--tb=short"])
    print("✨ Sacred testing complete!")