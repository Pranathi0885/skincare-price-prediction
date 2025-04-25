import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_and_click_load_more(driver, scroll_pause=1):
    """
    Scrolls slowly until the 'Load More' button becomes visible and clickable,
    then clicks it. Keeps scrolling without any limit until the button appears.
    """
    print("🔽 Scrolling down slowly to find 'Load More'...")
    l = 8
    while l:
        try:
            # Find the Load More button
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.lm-btm"))
            )
            
            # Scroll the Load More button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)  # Wait for the button to fully be in view
            
            # Click the 'Load More' button
            print("✅ 'Load More' button found. Clicking...")
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)  # Wait for the page to load the new items
            l -= 1  # Decrement the loop counter
        
        except Exception as e:
            # If not found, scroll more and retry
            print("⚠️ Error: Scrolling more...")
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(scroll_pause)
    return True


def get_skincare_product_info():
    driver = webdriver.Chrome()
    driver.get("https://www.purplle.com/skin/moisturizers")
    time.sleep(5)  # Allow the page to load
        
        
    scroll_and_click_load_more(driver)

    # Count the products after Load More
    time.sleep(2)
    products = driver.find_elements(By.CSS_SELECTOR, "div[id^='lp-itm-']")
    print(f"🧾 Total products currently visible: {len(products)}")

    
    product_data = []
    product_count = 0

    while product_count < 150:  # Continue scraping until we have 10 products
        # Scroll the page to load more products if lazy loading is involved
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for the products to load

        # Find all product elements
        products = driver.find_elements(By.CSS_SELECTOR, "app-listing-item")

        for product in products[product_count:]:
            try:
                title = product.find_element(By.CLASS_NAME, "product-title").text.strip()
                price = product.find_element(By.CLASS_NAME, "fw-bolder").text.strip()
                try:
                    original_price = product.find_element(By.TAG_NAME, "s").text.strip()
                except:
                    original_price = "N/A"
                try:
                    rating = product.find_element(By.CLASS_NAME, "star-rating").text.strip()
                except:
                    rating = "No rating"
                try:
                    reviews = product.find_element(By.CSS_SELECTOR, ".text-black-50.ms-1.fs-8").text.strip("() ")
                except:
                    reviews = "No reviews"

                # Open product page to extract specifications
                link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

                specifications = {}
                try:
                    spec_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'box__iterate-text')]"))
                    )
                    spec_rows = spec_box.find_elements(By.XPATH, ".//div[contains(@class, 'd-flex') and contains(@class, 'align-item-center')]")

                    for row in spec_rows:
                        key = row.find_element(By.XPATH, ".//span[1]").text.strip()
                        value = row.find_element(By.XPATH, ".//span[2]").text.strip()
                        specifications[key] = value

                except Exception as e:
                    specifications = {"Specifications": "Not found"}

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Combine all info, without 'Link'
                info = {
                    "Name": title,
                    "Price": price,
                    "Original Price": original_price,
                    "Rating": rating,
                    "Reviews": reviews
                }
                info.update(specifications)  # Merge specification details into main info
                product_data.append(info)
                product_count += 1  # Increase product count after successful extraction

                if product_count >= 150:
                    break  # Exit the loop if we've collected 10 products

            except Exception as e:
                print(f"Error reading product: {e}")
                continue  # Continue scraping next products even if an error occurs for a product

    driver.quit()
    return product_data

if __name__ == "__main__":
    product_data = get_skincare_product_info()

    if not product_data:
        print("No data collected. Please check website structure or CSS classes.")
    else:
        df = pd.DataFrame(product_data)
        
        # Remove the 'Link' column if it exists
        if 'Link' in df.columns:
            df.drop('Link', axis=1, inplace=True)

        csv_file_path = "m6.csv"
        df.to_csv(csv_file_path, index=False)

        print(f"\n✅ CSV file saved: {csv_file_path}")
        print(df.head())  # Print the first 5 rows for verification
