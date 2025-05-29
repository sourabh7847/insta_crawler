# test_crawler.py
"""Simple test script to verify crawler functionality"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_basic_setup():
    """Test if Selenium and ChromeDriver are working"""
    print("🧪 Testing basic setup...")
    
    try:
        # Set up driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        # Test navigation
        driver.get("https://www.google.com")
        print("✅ Successfully opened Google")
        
        # Test Instagram access
        driver.get("https://www.instagram.com")
        time.sleep(3)
        print("✅ Successfully accessed Instagram")
        
        print("🎉 Basic setup test passed!")
        
        # Close browser
        driver.quit()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_basic_setup()