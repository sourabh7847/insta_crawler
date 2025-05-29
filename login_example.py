# login_example.py
"""Example script demonstrating Instagram login functionality"""

from instagram_crawler import InstagramCrawler
from login_utils import get_login_credentials, validate_credentials, SecureCredentials
import time

def demo_login():
    """Demonstrate login functionality"""
    print("🔐 Instagram Login Demo")
    print("=" * 40)
    
    crawler = InstagramCrawler()
    
    try:
        # Method 1: Get credentials interactively
        print("\n📝 Getting login credentials...")
        username, password = get_login_credentials()
        
        # Validate credentials format
        is_valid, message = validate_credentials(username, password)
        if not is_valid:
            print(f"❌ Credential validation failed: {message}")
            return
        
        print(f"✅ {message}")
        
        # Attempt login
        print(f"\n🔑 Attempting login for user: {username}")
        if crawler.login(username, password):
            print("✅ Login successful!")
            
            # Handle post-login challenges
            crawler.handle_login_challenges()
            
            # Now you can access private profiles or get more data
            print("\n🎯 You can now:")
            print("- Search for private profiles")
            print("- Get follower/following lists (if permitted)")
            print("- Access more detailed profile information")
            
            # Example: Navigate to user's own profile
            own_profile_url = f"https://www.instagram.com/{username}/"
            crawler.driver.get(own_profile_url)
            time.sleep(3)
            
            print(f"\n📊 Navigated to your profile: {username}")
            
        else:
            print("❌ Login failed!")
            
    except Exception as e:
        print(f"❌ Error during login demo: {e}")
    
    finally:
        input("\nPress Enter to close browser...")
        crawler.close()

def demo_credential_management():
    """Demonstrate credential management features"""
    print("\n🔧 Credential Management Demo")
    print("=" * 40)
    
    secure_creds = SecureCredentials()
    
    # Demo saving credentials
    print("\n1. Saving test credentials...")
    test_username = "test_user"
    test_password = "test_password_123"
    
    if secure_creds.save_credentials(test_username, test_password):
        print("✅ Test credentials saved")
        
        # Demo loading credentials
        print("\n2. Loading saved credentials...")
        loaded_username, loaded_password = secure_creds.load_credentials()
        
        if loaded_username and loaded_password:
            print(f"✅ Loaded username: {loaded_username}")
            print("✅ Password loaded successfully (hidden)")
        
        # Demo deleting credentials
        print("\n3. Cleaning up test credentials...")
        secure_creds.delete_credentials()

def main():
    """Main function with menu options"""
    print("🚀 Instagram Login System")
    print("=" * 40)
    print("1. Demo login functionality")
    print("2. Demo credential management")
    print("3. Quick login test")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        demo_login()
    elif choice == "2":
        demo_credential_management()
    elif choice == "3":
        quick_login_test()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

def quick_login_test():
    """Quick test to verify login works"""
    print("\n⚡ Quick Login Test")
    print("=" * 30)
    
    crawler = InstagramCrawler()
    
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if crawler.login(username, password):
            print("✅ Login test passed!")
            crawler.handle_login_challenges()
        else:
            print("❌ Login test failed!")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    finally:
        crawler.close()

if __name__ == "__main__":
    main()