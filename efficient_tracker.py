from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import json
from datetime import datetime
import os
import sys
import re
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('product_tracking.log'),
        logging.StreamHandler()
    ]
)

class ProductTracker:
    def __init__(self, product_url, product_name):
        self.product_url = product_url
        self.product_name = product_name
        self.driver = None
        self.last_price = None
        self.price_history = []
        self.setup_driver()

    def setup_driver(self):
        """Initialize Chrome WebDriver with Windows-specific optimizations"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')  # New headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Windows-specific optimizations
            if platform.system() == 'Windows':
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-software-rasterizer')
                chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            
            # Initialize ChromeDriverManager without cache_valid_range
            service = Service(ChromeDriverManager().install())
            
            # Initialize driver with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    logging.info("WebDriver initialized successfully")
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(2)  # Wait before retry
                    
        except Exception as e:
            logging.error(f"Error initializing WebDriver: {str(e)}")
            raise

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

    def get_product_data(self):
        """Get current product data including price and availability"""
        try:
            self.driver.get(self.product_url)
            
            # Wait for the page to load with increased timeout
            WebDriverWait(self.driver, 15).until(
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
                ".a-price .a-price-whole"
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

            # Get product title
            try:
                title = self.driver.find_element(By.ID, "productTitle").text.strip()
            except NoSuchElementException:
                title = self.product_name

            product_data = {
                'timestamp': datetime.now().isoformat(),
                'title': title,
                'price': price,
                'availability': availability,
                'url': self.product_url
            }

            return product_data

        except TimeoutException:
            logging.error("Timeout while loading product page")
            return None
        except Exception as e:
            logging.error(f"Error getting product data: {str(e)}")
            return None

    def save_product_data(self, product_data):
        """Save product data to JSON file"""
        try:
            with open('product_history.json', 'a', encoding='utf-8') as f:
                json.dump(product_data, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            logging.error(f"Error saving product data: {str(e)}")

    def display_product_info(self, product_data):
        """Display product information in the console"""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "="*50)
            print(f"Real-time Product Tracker - {product_data['title']}")
            print("="*50)
            print(f"\nCurrent Price: ₹{product_data['price']:,.2f}")
            print(f"Availability: {product_data['availability']}")
            print(f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if self.last_price is not None:
                price_change = product_data['price'] - self.last_price
                change_percentage = (price_change / self.last_price) * 100
                print(f"\nPrice Change: {'+' if price_change > 0 else ''}₹{price_change:,.2f}")
                print(f"Change Percentage: {'+' if price_change > 0 else ''}{change_percentage:.2f}%")
            
            print("\nPrice History (Last 5 changes):")
            for entry in self.price_history[-5:]:
                print(f"{entry['timestamp']}: ₹{entry['price']:,.2f}")
            
            print("\n" + "="*50)
            print("Press Ctrl+C to stop tracking")
            print("="*50)
        except Exception as e:
            logging.error(f"Error displaying product info: {str(e)}")

    def track_product(self, interval=60):
        """
        Track product changes at regular intervals
        :param interval: Time interval between checks (in seconds)
        """
        try:
            print("Starting real-time product tracking...")
            print("Press Ctrl+C to stop")
            
            while True:
                try:
                    product_data = self.get_product_data()
                    if product_data:
                        current_price = product_data['price']
                        
                        # Save the product data
                        self.save_product_data(product_data)
                        
                        # Add to price history
                        self.price_history.append(product_data)
                        
                        # Display in console
                        self.display_product_info(product_data)
                        
                        self.last_price = current_price
                    
                    time.sleep(interval)
                except Exception as e:
                    logging.error(f"Error in tracking loop: {str(e)}")
                    time.sleep(5)  # Wait before retry
                
        except KeyboardInterrupt:
            print("\nProduct tracking stopped by user")
            logging.info("Product tracking stopped by user")
        finally:
            self.close()

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("WebDriver closed successfully")
            except Exception as e:
                logging.error(f"Error closing WebDriver: {str(e)}")

def main():
    # Example usage
    product_url = "https://www.amazon.in/Samsung-Smartphone-Titanium-Silverblue-Included/dp/B0DSKNVWK7"
    product_name = "Samsung Galaxy S25 Ultra"
    
    try:
        tracker = ProductTracker(product_url, product_name)
        # Start tracking product changes every minute
        tracker.track_product(interval=60)
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Main execution error: {str(e)}")
    finally:
        if 'tracker' in locals():
            tracker.close()

if __name__ == "__main__":
    main() 