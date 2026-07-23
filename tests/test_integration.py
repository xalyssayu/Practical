import pytest
import requests
import json

BASE_URL = "http://localhost:5000"

class TestIntegration:
    """Integration tests for the Secure Password App"""

    def test_home_page(self):
        """Test that the home page loads"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert "Secure Password App" in response.text

    def test_login_page(self):
        """Test that the login page loads"""
        response = requests.get(f"{BASE_URL}/login")
        assert response.status_code == 200
        assert "Login" in response.text

    def test_register_page(self):
        """Test that the register page loads"""
        response = requests.get(f"{BASE_URL}/register")
        assert response.status_code == 200
        assert "Register" in response.text

    def test_password_strength_api(self):
        """Test the password strength API endpoint"""
        data = {"password": "SecurePassword123!"}
        response = requests.post(
            f"{BASE_URL}/password-strength",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "strength" in result
        assert "valid" in result

    def test_registration_flow(self):
        """Test user registration"""
        test_user = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "confirm_password": "SecurePassword123!"
        }
        # This would need a proper test user creation
        # For now, we test the endpoint
        response = requests.post(
            f"{BASE_URL}/register",
            data=test_user
        )
        # Should redirect or show success
        assert response.status_code in [200, 302]

    def test_weak_password_rejection(self):
        """Test that weak passwords are rejected"""
        weak_passwords = [
            "password",
            "12345678",
            "qwerty",
            "abc123",
            "letmein"
        ]
        for pwd in weak_passwords:
            data = {"password": pwd}
            response = requests.post(
                f"{BASE_URL}/password-strength",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            result = response.json()
            # Weak passwords should be invalid
            assert result["valid"] == False or result["strength"] < 50