from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import getpass
import os
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Suppress various logging messages
os.environ['WDM_LOG'] = '0'
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

class InstagramCrawler:
    def __init__(self):
        """Initialize the Instagram crawler with Chrome driver"""
        self.driver = None
        self.is_logged_in = False
        self.setup_driver()
    
    def setup_driver(self):
        """Set up Chrome driver with basic options"""
        try:
            # Chrome options for better performance and stealth
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Suppress logging messages
            chrome_options.add_argument("--log-level=3")  # Suppress INFO, WARNING, ERROR
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-logging-redirect")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--silent")
            
            # Uncomment the line below to run in headless mode (no browser window)
            # chrome_options.add_argument("--headless")
            
            # Set up the driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to avoid detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            sys.exit(1)
    
    def login(self, username, password):
        """Login to Instagram with username and password"""
        try:
            print("🔐 Attempting to login...")
            
            # Navigate to login page
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for login form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            time.sleep(2)
            
            # Find username and password fields
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Clear fields and enter credentials
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(1)
            
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Find and click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to process
            time.sleep(5)
            
            # Check if login was successful
            if self.check_login_success():
                print("✅ Login successful!")
                self.is_logged_in = True
                return True
            else:
                print("❌ Login failed - check credentials")
                return False
                
        except TimeoutException:
            print("❌ Login timeout - page took too long to load")
            return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def check_login_success(self):
        """Check if login was successful by looking for indicators"""
        try:
            # Check if we're redirected to home page or if there are error messages
            current_url = self.driver.current_url
            
            # If still on login page, check for error messages
            if "login" in current_url:
                try:
                    # Look for error messages
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                        "div[role='alert'], .error-message, p[data-testid='login-error-message']")
                    if error_elements:
                        error_text = error_elements[0].text
                        print(f"❌ Login error: {error_text}")
                        return False
                except:
                    pass
                
                # Still on login page without clear error - likely failed
                return False
            
            # Check for common post-login elements
            try:
                # Look for home page indicators
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']"))
                    )
                )
                return True
            except:
                return False
                
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
    
    def handle_login_challenges(self):
        """Handle common login challenges like 2FA, suspicious login, etc."""
        try:
            print("🔍 Checking for login challenges...")
            
            # Check for 2FA/verification code
            if self.driver.find_elements(By.CSS_SELECTOR, "input[name='verificationCode']"):
                print("📱 Two-factor authentication detected")
                verification_code = input("Enter verification code from your phone: ").strip()
                
                if verification_code:
                    code_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='verificationCode']")
                    code_field.send_keys(verification_code)
                    
                    # Click confirm button
                    confirm_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    confirm_button.click()
                    time.sleep(5)
                    
                    return self.check_login_success()
            
            # Check for "Save Login Info" prompt
            try:
                save_info_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                for button in save_info_buttons:
                    if "Not Now" in button.text or "Save Info" in button.text:
                        if "Not Now" in button.text:
                            button.click()
                            time.sleep(2)
                            break
            except:
                pass
            
            # Check for "Turn on Notifications" prompt
            try:
                notification_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                for button in notification_buttons:
                    if "Not Now" in button.text:
                        button.click()
                        time.sleep(2)
                        break
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"Error handling login challenges: {e}")
            return False
        """Navigate to Instagram homepage"""
        try:
            print("🌐 Visiting Instagram...")
            self.driver.get("https://www.instagram.com")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Instagram loaded successfully")
            time.sleep(3)  # Give page time to fully render
            
        except Exception as e:
            print(f"❌ Error visiting Instagram: {e}")
    
    def search_profile(self, username):
        """Search for a specific Instagram profile"""
        try:
            print(f"🔍 Searching for profile: {username}")
            
            # Look for search input (Instagram's search box)
            search_selectors = [
                "input[placeholder*='Search']",
                "input[aria-label*='Search']",
                "input[placeholder*='search']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not search_input:
                print("❌ Could not find search input")
                return False
            
            # Clear and enter username
            search_input.clear()
            search_input.send_keys(username)
            time.sleep(2)
            
            # Press Enter to search
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
            
            print(f"✅ Search initiated for: {username}")
            return True
            
        except Exception as e:
            print(f"❌ Error searching for profile: {e}")
            return False
    
    def get_profile_info(self):
        """Extract basic profile information from current page"""
        try:
            print("📊 Extracting profile information...")
            
            # Wait for profile page to load
            time.sleep(3)
            
            profile_info = {}
            
            # Try to get username
            try:
                username_element = self.driver.find_element(By.CSS_SELECTOR, "h2")
                profile_info['username'] = username_element.text
            except:
                profile_info['username'] = "Not found"
            
            # Try to get follower count, following count, posts count
            try:
                stats = self.driver.find_elements(By.CSS_SELECTOR, "a span")
                if len(stats) >= 3:
                    profile_info['posts'] = stats[0].text
                    profile_info['followers'] = stats[1].text
                    profile_info['following'] = stats[2].text
            except:
                profile_info['posts'] = "Not found"
                profile_info['followers'] = "Not found" 
                profile_info['following'] = "Not found"
            
            # Try to get bio
            try:
                bio_element = self.driver.find_element(By.CSS_SELECTOR, "div._aa_c span")
                profile_info['bio'] = bio_element.text
            except:
                profile_info['bio'] = "Not found"
            
            return profile_info
            
        except Exception as e:
            print(f"❌ Error extracting profile info: {e}")
            return {}
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function to run the crawler"""
    crawler = InstagramCrawler()
    
    try:
        print("🚀 Instagram Profile Crawler")
        print("=" * 40)
        
        # Ask user for login preference
        login_choice = input("Do you want to login? (y/n): ").strip().lower()
        
        if login_choice == 'y':
            # Get login credentials
            username = input("Enter your Instagram username: ").strip()
            password = getpass.getpass("Enter your Instagram password: ")
            
            if not username or not password:
                print("❌ Username and password are required")
                return
            
            # Attempt login
            if crawler.login(username, password):
                # Handle any post-login challenges
                crawler.handle_login_challenges()
            else:
                print("❌ Login failed. Continuing without login...")
                crawler.visit_instagram()
        else:
            # Visit Instagram without login
            crawler.visit_instagram()
        
        # Get target profile username
        target_username = input("\nEnter Instagram username to search: ").strip()
        
        if not target_username:
            print("❌ No username provided")
            return
        
        # Search for profile (try direct navigation first)
        if crawler.search_profile(target_username):
            # Wait a bit for profile to load
            time.sleep(3)
            
            # Get profile information
            profile_info = crawler.get_profile_info()
            
            if profile_info:
                print("\n" + "="*50)
                print("PROFILE INFORMATION")
                print("="*50)
                for key, value in profile_info.items():
                    print(f"{key.capitalize()}: {value}")
                print("="*50)
            
            # If logged in, can potentially access more information
            if crawler.is_logged_in:
                print("\n💡 Logged in - you may have access to additional profile information")
        else:
            # Try direct URL method as fallback
            print("🔄 Trying direct URL method...")
            profile_url = f"https://www.instagram.com/{target_username}/"
            crawler.driver.get(profile_url)
            time.sleep(5)
            
            # Check if profile exists
            if "Page Not Found" not in crawler.driver.page_source and "Sorry, this page isn't available" not in crawler.driver.page_source:
                profile_info = crawler.get_profile_info()
                if profile_info:
                    print("\n" + "="*50)
                    print("PROFILE INFORMATION")
                    print("="*50)
                    for key, value in profile_info.items():
                        print(f"{key.capitalize()}: {value}")
                    print("="*50)
            else:
                print(f"❌ Profile '{target_username}' not found")
        
        # Keep browser open for manual inspection
        input("\nPress Enter to close the browser...")
        
    except KeyboardInterrupt:
        print("\n⚠️ Crawler interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        crawler.close()

if __name__ == "__main__":
    main()