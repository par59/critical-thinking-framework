from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('website_tracking.log'),
        logging.StreamHandler()
    ]
)

class WebsiteTracker:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        logging.info("WebDriver initialized successfully")

    def track_element(self, element_selector, selector_type=By.CSS_SELECTOR, timeout=10):
        """
        Track a specific element on the website
        :param element_selector: CSS selector or XPath of the element
        :param selector_type: Type of selector (By.CSS_SELECTOR or By.XPATH)
        :param timeout: Maximum time to wait for the element
        """
        try:
            self.driver.get(self.url)
            logging.info(f"Navigated to {self.url}")
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((selector_type, element_selector))
            )
            logging.info(f"Element found: {element_selector}")
            
            # Track element properties
            element_properties = {
                'text': element.text,
                'location': element.location,
                'size': element.size,
                'is_displayed': element.is_displayed(),
                'is_enabled': element.is_enabled()
            }
            
            logging.info(f"Element properties: {element_properties}")
            return element_properties
            
        except TimeoutException:
            logging.error(f"Element not found: {element_selector}")
            return None
        except Exception as e:
            logging.error(f"Error tracking element: {str(e)}")
            return None

    def track_page_changes(self, interval=5, duration=60):
        """
        Track changes on the page at regular intervals
        :param interval: Time interval between checks (in seconds)
        :param duration: Total duration to track (in seconds)
        """
        try:
            self.driver.get(self.url)
            logging.info(f"Starting page tracking for {duration} seconds")
            
            start_time = time.time()
            while time.time() - start_time < duration:
                page_source = self.driver.page_source
                logging.info(f"Page source length: {len(page_source)}")
                time.sleep(interval)
                
        except Exception as e:
            logging.error(f"Error during page tracking: {str(e)}")

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed successfully")

def main():
    # Example usage
    tracker = WebsiteTracker("https://example.com")
    
    try:
        # Track a specific element
        element_properties = tracker.track_element("#some-element")
        
        # Track page changes
        tracker.track_page_changes(interval=5, duration=60)
        
    finally:
        tracker.close()

if __name__ == "__main__":
    product_urls = [
        "https://www.amazon.com/dp/YOUR-PRODUCT-ID-1",
        "https://www.amazon.com/dp/YOUR-PRODUCT-ID-2",
    ]
    main() 