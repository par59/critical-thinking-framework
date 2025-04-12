from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Setup browser options
options = Options()
options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

# Target search query
query = "kurta"
driver.get(f"https://www.flipkart.com/search?q={query}")
time.sleep(3)

# Close login popup
try:
    driver.find_element(By.XPATH, "//button[contains(text(),'✕')]").click()
    time.sleep(1)
except:
    pass

# Scroll down to load more
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Target all product cards (grid view layout)
product_cards = driver.find_elements(By.XPATH, '//div[contains(@class,"_2B099V")] | //div[contains(@class,"_1xHGtK")]')

print(f"🛒 Found {len(product_cards)} product cards.")

data = []

for card in product_cards:
    try:
        name = card.find_element(By.CLASS_NAME, "IRpwTa").text
    except:
        name = "N/A"

    try:
        price = card.find_element(By.CLASS_NAME, "_30jeq3").text
    except:
        price = "N/A"

    try:
        rating = card.find_element(By.CLASS_NAME, "_3LWZlK").text
    except:
        rating = "N/A"

    try:
        link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = "N/A"

    # Only add if product name is valid
    if name != "N/A" and price != "N/A":
        data.append({
            "Product": name,
            "Price": price,
            "Rating": rating,
            "Link": link
        })

driver.quit()

# Save results
df = pd.DataFrame(data).drop_duplicates()

if not df.empty:
    df.to_excel("flipkart_kurta_clean.xlsx", index=False)
    print("✅ Success! Saved to 'flipkart_kurta_clean.xlsx'")
else:
    print("⚠️ Still no usable product data. Flipkart may be limiting access.")
