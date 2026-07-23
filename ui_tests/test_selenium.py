import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

FLASK_URL = os.environ.get("FLASK_URL", "http://localhost:5000")
SELENIUM_HUB = os.environ.get("SELENIUM_HUB", "http://localhost:4444/wd/hub")

class TestUI:
    """UI tests for the Secure Password App using Selenium"""

    @pytest.fixture
    def driver(self):
        """Set up Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        
        driver = webdriver.Remote(
            command_executor=SELENIUM_HUB,
            options=options
        )
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_home_page_loads(self, driver):
        """Test that the home page loads correctly"""
        driver.get(f"{FLASK_URL}/")
        assert "Secure Password App" in driver.page_source
        assert "Login" in driver.page_source
        assert "Register" in driver.page_source

    def test_login_page_has_form(self, driver):
        """Test that the login page has username and password fields"""
        driver.get(f"{FLASK_URL}/login")
        
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        assert username_field is not None
        assert password_field is not None
        assert submit_button is not None

    def test_register_page_loads(self, driver):
        """Test that the register page loads correctly"""
        driver.get(f"{FLASK_URL}/register")
        assert "Register" in driver.page_source
        assert "username" in driver.page_source
        assert "email" in driver.page_source
        assert "password" in driver.page_source

    def test_user_registration_flow(self, driver):
        """Test the full user registration flow"""
        driver.get(f"{FLASK_URL}/register")
        
        # Fill registration form
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_field = driver.find_element(By.NAME, "confirm_password")
        
        username_field.send_keys("selenium_test_user")
        email_field.send_keys("selenium@test.com")
        password_field.send_keys("SecurePassword123!")
        confirm_field.send_keys("SecurePassword123!")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for page to load
        time.sleep(2)
        
        # Should be redirected to login page or show success
        assert "Login" in driver.page_source or "Registration successful" in driver.page_source

    def test_login_flow(self, driver):
        """Test login with valid credentials"""
        # First, register a user
        driver.get(f"{FLASK_URL}/register")
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_field = driver.find_element(By.NAME, "confirm_password")
        
        username_field.send_keys("selenium_login_user")
        email_field.send_keys("selenium_login@test.com")
        password_field.send_keys("SecurePassword123!")
        confirm_field.send_keys("SecurePassword123!")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(2)
        
        # Now login
        driver.get(f"{FLASK_URL}/login")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys("selenium_login_user")
        password_field.send_keys("SecurePassword123!")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        time.sleep(2)
        
        # Should reach dashboard
        assert "Welcome" in driver.page_source

    def test_password_strength_check(self, driver):
        """Test the password strength indicator"""
        driver.get(f"{FLASK_URL}/register")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("SecurePassword123!")
        
        # Wait for strength indicator to update
        time.sleep(2)
        
        # Check if strength indicator is present
        strength_text = driver.find_element(By.ID, "strength-text").text
        assert "Strong" in strength_text or "Good" in strength_text or "Very Strong" in strength_text

    def test_logout_functionality(self, driver):
        """Test the logout functionality"""
        # Register and login first
        driver.get(f"{FLASK_URL}/register")
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_field = driver.find_element(By.NAME, "confirm_password")
        
        username_field.send_keys("selenium_logout_user")
        email_field.send_keys("selenium_logout@test.com")
        password_field.send_keys("SecurePassword123!")
        confirm_field.send_keys("SecurePassword123!")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(2)
        
        driver.get(f"{FLASK_URL}/login")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys("selenium_logout_user")
        password_field.send_keys("SecurePassword123!")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        time.sleep(2)
        
        # Click logout
        logout_link = driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()
        time.sleep(2)
        
        # Should be back to home page
        assert "Secure Password App" in driver.page_source