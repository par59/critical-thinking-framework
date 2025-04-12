from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecommerce_tracking.log'),
        logging.StreamHandler()
    ]
)

class EcommerceTracker:
    def __init__(self):
        self.driver = None
        self.setup_driver()

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

    def track_product(self, product_url):
        """
        Track product details from Amazon
        :param product_url: URL of the product to track
        """
        try:
            self.driver.get(product_url)
            logging.info(f"Navigated to product page: {product_url}")
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )

            # Extract product information
            product_data = {
                'timestamp': datetime.now().isoformat(),
                'title': self.driver.find_element(By.ID, "productTitle").text.strip(),
                'price': self._get_price(),
                'availability': self._get_availability(),
                'rating': self._get_rating(),
                'review_count': self._get_review_count(),
                'url': product_url
            }

            # Save the data
            self._save_product_data(product_data)
            logging.info(f"Product data collected: {product_data['title']}")
            return product_data

        except TimeoutException:
            logging.error("Timeout while loading product page")
            return None
        except Exception as e:
            logging.error(f"Error tracking product: {str(e)}")
            return None

    def _get_price(self):
        """Extract product price"""
        try:
            price_element = self.driver.find_element(By.CSS_SELECTOR, "span.a-price-whole")
            return price_element.text.strip()
        except:
            return "Price not found"

    def _get_availability(self):
        """Extract product availability"""
        try:
            availability = self.driver.find_element(By.ID, "availability").text.strip()
            return availability
        except:
            return "Availability not found"

    def _get_rating(self):
        """Extract product rating"""
        try:
            rating = self.driver.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
            return rating.split()[0]
        except:
            return "Rating not found"

    def _get_review_count(self):
        """Extract number of reviews"""
        try:
            review_count = self.driver.find_element(By.ID, "acrCustomerReviewText").text
            return review_count.split()[0]
        except:
            return "Review count not found"

    def _save_product_data(self, data):
        """Save product data to a JSON file"""
        try:
            with open('product_tracking.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
        except Exception as e:
            logging.error(f"Error saving product data: {str(e)}")

    def track_multiple_products(self, product_urls, interval=300):
        """
        Track multiple products at regular intervals
        :param product_urls: List of product URLs to track
        :param interval: Time interval between checks (in seconds)
        """
        try:
            while True:
                for url in product_urls:
                    self.track_product(url)
                    time.sleep(5)  # Small delay between products
                logging.info(f"Waiting {interval} seconds before next check...")
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Tracking stopped by user")
        finally:
            self.close()

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed successfully")

def main():
    # Example product URLs to track
    product_urls = [
        "https://www.amazon.com/dp/B08N5KWB9H",  # Example product 1
        "https://www.amazon.com/dp/B08N5KWB9H",  # Example product 2
    ]
    
    tracker = EcommerceTracker()
    try:
        # Track multiple products
        tracker.track_multiple_products(product_urls, interval=300)  # Check every 5 minutes
    except KeyboardInterrupt:
        logging.info("Tracking stopped by user")
    finally:
        tracker.close()

if __name__ == "__main__":
    main() 