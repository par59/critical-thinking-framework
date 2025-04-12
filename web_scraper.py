from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_flipkart(search_term, num_products=5):
    # Set up Chrome options
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Go to Flipkart
        driver.get('https://www.flipkart.com')
        
        # Handle login popup
        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_2KpZ6l _2doB4z"]')))
            close_btn.click()
        except:
            pass
        
        # Find search box and search for product
        search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
        search_box.send_keys(search_term)
        search_box.submit()
        
        # Wait for results to load
        time.sleep(3)
        
        # Initialize lists to store product data
        names = []
        prices = []
        ratings = []
        num_reviews = []
        
        # Find all product containers
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._1AtVbE')))
        
        # Process only the required number of products
        for product in products[:num_products]:
            try:
                # Scroll product into view
                driver.execute_script("arguments[0].scrollIntoView();", product)
                time.sleep(1)
                
                # Get product name
                try:
                    name = product.find_element(By.CSS_SELECTOR, 'div._4rR01T').text
                except:
                    try:
                        name = product.find_element(By.CSS_SELECTOR, 'a.s1Q9rs').text
                    except:
                        continue
                
                # Get product price
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, 'div._30jeq3').text
                    price = int(price_text.replace('₹', '').replace(',', ''))
                except:
                    continue
                
                # Get rating
                try:
                    rating_text = product.find_element(By.CSS_SELECTOR, 'div._3LWZlK').text
                    rating = float(rating_text)
                except:
                    rating = 0
                
                # Get number of reviews
                try:
                    reviews_text = product.find_element(By.CSS_SELECTOR, 'span._2_R_DZ').text
                    reviews = int(reviews_text.split()[0].replace(',', ''))
                except:
                    reviews = 0
                
                # Append data to lists
                names.append(name)
                prices.append(price)
                ratings.append(rating)
                num_reviews.append(reviews)
                
                print(f"Scraped: {name}")
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue
        
        # Create DataFrame
        data = {
            'Product Name': names,
            'Price': prices,
            'Rating': ratings,
            'Number of Reviews': num_reviews
        }
        
        df = pd.DataFrame(data)
        
        # Save to CSV
        filename = f'flipkart_{search_term.replace(" ", "_")}.csv'
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        
        return df
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
    finally:
        driver.quit()

if __name__ == "__main__":
    # Test the scraper
    search_term = "gaming laptop"
    print(f"\nScraping Flipkart for: {search_term}")
    df = scrape_flipkart(search_term, 5)
    
    if df is not None and not df.empty:
        print("\nScraped Data:")
        print(df)
    else:
        print("No data was scraped") 