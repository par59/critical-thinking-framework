from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import json
from datetime import datetime
import os
import sys
import re
from twilio.rest import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('samsung_price_tracking.log'),
        logging.StreamHandler()
    ]
)

class SamsungPriceTracker:
    def __init__(self, whatsapp_config=None):
        self.driver = None
        self.setup_driver()
        self.whatsapp_config = whatsapp_config
        self.last_price = None
        self.product_url = "https://www.amazon.in/Samsung-Smartphone-Titanium-Silverblue-Included/dp/B0DSKNVWK7"
        self.product_name = "Samsung Galaxy S25 Ultra"
        self.price_history = []
        self.start_time = datetime.now()

    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # Add these options to avoid detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        # Modify the navigator.webdriver flag to prevent detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        logging.info("WebDriver initialized successfully")

    def clear_console(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def extract_price(self, price_text):
        """Extract price from text and convert to float"""
        try:
            # Remove currency symbol and commas
            price_text = price_text.replace('₹', '').replace(',', '').strip()
            # Extract numbers and decimal point
            price_match = re.search(r'[\d,]+(\.\d+)?', price_text)
            if price_match:
                return float(price_match.group())
            return None
        except Exception as e:
            logging.error(f"Error extracting price: {str(e)}")
            return None

    def get_current_price(self):
        """Get the current price of the product"""
        try:
            self.driver.get(self.product_url)
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )

            # Try different price selectors
            price = None
            price_selectors = [
                "span.a-price-whole",
                "span.a-offscreen",
                "#priceblock_ourprice",
                "#priceblock_dealprice",
                "#priceblock_saleprice",
                ".a-price .a-offscreen",
                ".a-price .a-price-whole",
                "#price_inside_buybox",
                "#priceblock_ourprice_lbl",
                "#priceblock_dealprice_lbl",
                "#priceblock_saleprice_lbl",
                ".a-price .a-price-symbol",
                ".a-price .a-price-fraction"
            ]

            for selector in price_selectors:
                try:
                    price_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text
                    if price_text:
                        price = self.extract_price(price_text)
                        if price:
                            break
                except NoSuchElementException:
                    continue

            if not price:
                # Try to find price in the page source
                page_source = self.driver.page_source
                price_match = re.search(r'₹\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', page_source)
                if price_match:
                    price = self.extract_price(price_match.group())
            
            if not price:
                logging.error("Could not find price on the page")
                return None
            
            # Get availability
            try:
                availability = self.driver.find_element(By.ID, "availability").text.strip()
            except NoSuchElementException:
                try:
                    availability = self.driver.find_element(By.CSS_SELECTOR, ".a-size-medium.a-color-success").text.strip()
                except NoSuchElementException:
                    availability = "Availability not found"

            price_data = {
                'timestamp': datetime.now().isoformat(),
                'price': price,
                'availability': availability
            }

            # Add to price history
            self.price_history.append(price_data)
            
            # Display in console
            self.display_price_info(price_data)
            
            return price_data

        except TimeoutException:
            logging.error("Timeout while loading product page")
            return None
        except Exception as e:
            logging.error(f"Error getting price: {str(e)}")
            return None

    def display_price_info(self, price_data):
        """Display price information in the console"""
        self.clear_console()
        print("\n" + "="*50)
        print(f"Real-time Price Tracker - {self.product_name}")
        print("="*50)
        print(f"\nCurrent Price: ₹{price_data['price']:,.2f}")
        print(f"Availability: {price_data['availability']}")
        print(f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.last_price is not None:
            price_change = price_data['price'] - self.last_price
            change_percentage = (price_change / self.last_price) * 100
            print(f"\nPrice Change: {'+' if price_change > 0 else ''}₹{price_change:,.2f}")
            print(f"Change Percentage: {'+' if price_change > 0 else ''}{change_percentage:.2f}%")
        
        print("\nPrice History (Last 5 changes):")
        for entry in self.price_history[-5:]:
            print(f"{entry['timestamp']}: ₹{entry['price']:,.2f}")
        
        print("\n" + "="*50)
        print("Press Ctrl+C to stop tracking")
        print("="*50)

    def save_price_data(self, price_data):
        """Save price data to JSON file"""
        try:
            with open('samsung_price_history.json', 'a') as f:
                json.dump(price_data, f)
                f.write('\n')
        except Exception as e:
            logging.error(f"Error saving price data: {str(e)}")

    def send_whatsapp_message(self, message):
        """Send WhatsApp message using Twilio"""
        if not self.whatsapp_config:
            logging.warning("WhatsApp configuration not set. Skipping notification.")
            return

        try:
            client = Client(self.whatsapp_config['account_sid'], self.whatsapp_config['auth_token'])
            message = client.messages.create(
                from_=f"whatsapp:{self.whatsapp_config['twilio_number']}",
                body=message,
                to=f"whatsapp:{self.whatsapp_config['your_number']}"
            )
            logging.info(f"WhatsApp message sent successfully: {message.sid}")
        except Exception as e:
            logging.error(f"Error sending WhatsApp message: {str(e)}")

    def send_initial_price_notification(self, price_data):
        """Send initial price notification via WhatsApp"""
        message = f"""
🚨 Price Tracking Started for {self.product_name}!

💰 Initial Price: ₹{price_data['price']:,.2f}
📦 Availability: {price_data['availability']}
⏰ Tracking Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

You will receive WhatsApp notifications whenever the price changes.

🔗 Product Link: {self.product_url}
"""
        self.send_whatsapp_message(message)

    def send_price_alert(self, current_price, previous_price):
        """Send price change alert via WhatsApp"""
        price_change = current_price - previous_price
        change_percentage = (price_change / previous_price) * 100
        change_type = "decreased" if price_change < 0 else "increased"
        emoji = "📉" if price_change < 0 else "📈"

        message = f"""
🚨 Price Alert for {self.product_name}!

💰 Current Price: ₹{current_price:,.2f}
💰 Previous Price: ₹{previous_price:,.2f}
📊 Price {change_type} by: ₹{abs(price_change):,.2f}
📈 Change Percentage: {change_percentage:.2f}%

🔗 Check the product here: {self.product_url}
"""
        self.send_whatsapp_message(message)

    def track_price(self, interval=60):
        """
        Track price changes at regular intervals
        :param interval: Time interval between checks (in seconds)
        """
        try:
            print("Starting real-time price tracking...")
            print("Press Ctrl+C to stop")
            
            # Get initial price and send notification
            initial_price_data = self.get_current_price()
            if initial_price_data:
                self.send_initial_price_notification(initial_price_data)
                self.last_price = initial_price_data['price']
            
            while True:
                price_data = self.get_current_price()
                if price_data:
                    current_price = price_data['price']
                    
                    # Save the price data
                    self.save_price_data(price_data)
                    
                    # Check for price change and send alert
                    if self.last_price is not None and current_price != self.last_price:
                        logging.info(f"Price changed from ₹{self.last_price:,.2f} to ₹{current_price:,.2f}")
                        self.send_price_alert(current_price, self.last_price)
                    
                    self.last_price = current_price
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nPrice tracking stopped by user")
            logging.info("Price tracking stopped by user")
        finally:
            self.close()

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed successfully")

def main():
    # WhatsApp configuration using Twilio
    whatsapp_config = {
        'account_sid': 'your_account_sid',  # Your Twilio Account SID
        'auth_token': 'your_auth_token',    # Your Twilio Auth Token
        'twilio_number': '+14155238886',    # Twilio's WhatsApp number
        'your_number': '+919876543210'      # Your WhatsApp number with country code
    }
    
    # Test WhatsApp configuration
    try:
        client = Client(whatsapp_config['account_sid'], whatsapp_config['auth_token'])
        test_message = client.messages.create(
            from_=f"whatsapp:{whatsapp_config['twilio_number']}",
            body="Test message from Samsung Price Tracker",
            to=f"whatsapp:{whatsapp_config['your_number']}"
        )
        print("WhatsApp configuration test successful!")
    except Exception as e:
        print(f"WhatsApp configuration error: {str(e)}")
        print("\nPlease follow these steps to set up Twilio for WhatsApp:")
        print("1. Sign up for a Twilio account at https://www.twilio.com")
        print("2. Get your Account SID and Auth Token from the Twilio Console")
        print("3. Enable WhatsApp in your Twilio account")
        print("4. Replace the configuration values in the script:")
        print("   - account_sid: Your Twilio Account SID")
        print("   - auth_token: Your Twilio Auth Token")
        print("   - your_number: Your WhatsApp number with country code (e.g., +919876543210)")
        return
    
    tracker = SamsungPriceTracker(whatsapp_config)
    try:
        # Start tracking price changes every minute
        tracker.track_price(interval=60)
    except KeyboardInterrupt:
        print("\nTracking stopped by user")
    finally:
        tracker.close()

if __name__ == "__main__":
    main() 