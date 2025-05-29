# login_utils.py
"""Utility functions for handling Instagram login securely"""

import json
import os
import getpass
from cryptography.fernet import Fernet
import base64

class SecureCredentials:
    """Handle secure storage and retrieval of login credentials"""
    
    def __init__(self, credentials_file="credentials.enc"):
        self.credentials_file = credentials_file
        self.key_file = "key.key"
    
    def generate_key(self):
        """Generate a new encryption key"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as key_file:
            key_file.write(key)
        return key
    
    def load_key(self):
        """Load the encryption key"""
        try:
            with open(self.key_file, 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            return self.generate_key()
    
    def save_credentials(self, username, password):
        """Save credentials securely"""
        try:
            key = self.load_key()
            f = Fernet(key)
            
            credentials = {
                'username': username,
                'password': password
            }
            
            # Encrypt the credentials
            encrypted_data = f.encrypt(json.dumps(credentials).encode())
            
            with open(self.credentials_file, 'wb') as file:
                file.write(encrypted_data)
            
            print("✅ Credentials saved securely")
            return True
            
        except Exception as e:
            print(f"❌ Error saving credentials: {e}")
            return False
    
    def load_credentials(self):
        """Load saved credentials"""
        try:
            if not os.path.exists(self.credentials_file):
                return None, None
            
            key = self.load_key()
            f = Fernet(key)
            
            with open(self.credentials_file, 'rb') as file:
                encrypted_data = file.read()
            
            # Decrypt the credentials
            decrypted_data = f.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return credentials['username'], credentials['password']
            
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            return None, None
    
    def delete_credentials(self):
        """Delete saved credentials"""
        try:
            if os.path.exists(self.credentials_file):
                os.remove(self.credentials_file)
            if os.path.exists(self.key_file):
                os.remove(self.key_file)
            print("✅ Saved credentials deleted")
        except Exception as e:
            print(f"❌ Error deleting credentials: {e}")

def get_login_credentials():
    """Get login credentials from user with option to save"""
    secure_creds = SecureCredentials()
    
    # Check if credentials are already saved
    saved_username, saved_password = secure_creds.load_credentials()
    
    if saved_username and saved_password:
        use_saved = input(f"Use saved credentials for '{saved_username}'? (y/n): ").strip().lower()
        if use_saved == 'y':
            return saved_username, saved_password
    
    # Get new credentials
    print("\nEnter your Instagram login credentials:")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    
    if username and password:
        save_creds = input("Save credentials securely for future use? (y/n): ").strip().lower()
        if save_creds == 'y':
            secure_creds.save_credentials(username, password)
    
    return username, password

def validate_credentials(username, password):
    """Basic validation of credentials format"""
    if not username or not password:
        return False, "Username and password cannot be empty"
    
    if len(username) < 1:
        return False, "Username too short"
    
    if len(password) < 6:
        return False, "Password too short (Instagram requires at least 6 characters)"
    
    # Check for common invalid characters in username
    invalid_chars = ['@', ' ', '#']
    for char in invalid_chars:
        if char in username:
            return False, f"Username contains invalid character: {char}"
    
    return True, "Credentials format is valid"

# Login strategies for different scenarios
class LoginStrategies:
    """Different login approaches for various situations"""
    
    @staticmethod
    def basic_login(driver, username, password):
        """Basic login method"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        
        try:
            # Navigate to login page
            driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for login form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Fill credentials
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys(username)
            time.sleep(1)
            password_field.send_keys(password)
            time.sleep(1)
            
            # Submit form
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            return True
            
        except Exception as e:
            print(f"Basic login failed: {e}")
            return False
    
    @staticmethod
    def slow_login(driver, username, password):
        """Slower, more human-like login method"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        import random
        
        try:
            # Navigate to login page
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(2, 4))
            
            # Wait for login form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Fill username slowly
            username_field = driver.find_element(By.NAME, "username")
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(1, 2))
            
            # Fill password slowly
            password_field = driver.find_element(By.NAME, "password")
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(1, 3))
            
            # Submit form
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            return True
            
        except Exception as e:
            print(f"Slow login failed: {e}")
            return False