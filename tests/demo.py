from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()

driver.maximize_window()

# Open flipkart.com
driver.get("https://www.flipkart.com")

# Search for the product "Samsung Galaxy S10"
search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
search_box.send_keys("Samsung Galaxy S10")
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# Click on "Mobiles" in categories
mobiles_category = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="container"]/div/div[3]/div[1]/div[1]/div/div[1]/div/div/section/div[3]/div/a',
        )
    )
)
mobiles_category.click()
time.sleep(2)

# Apply filters
brand_filter_checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="container"]/div/div[3]/div[1]/div[1]/div/div[1]/div/section[3]/div[2]/div/div/div/label/div[1]',
        )
    )
)
brand_filter_checkbox.click()
time.sleep(3)


flipkart_assured_filter = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="container"]/div/div[3]/div/div[1]/div/div[1]/div/section[4]/label/div[1]',
        )
    )
)
flipkart_assured_filter.click()
time.sleep(2)


# Sort by price high to low
sort_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="container"]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[4]',
        )
    )
)
sort_dropdown.click()
time.sleep(5)


# Get product details
product_elements = driver.find_elements(By.CLASS_NAME, "_1fQZEK")
time.sleep(2)
print(len(product_elements))

product_list = []

# Print the details
for product_element in product_elements:
    product_name = product_element.find_element(By.CLASS_NAME, "_4rR01T").text
    display_price = product_element.find_element(By.CLASS_NAME, "_30jeq3").text
    product_link = product_element.get_attribute("href")

    product_list.append(
        {
            "Product Name": product_name,
            "Display Price": display_price,
            "Link to Product Details Page": product_link,
        }
    )

    print(
        f"Product name:{product_name}\nDisplay price:{display_price}\nMore Details:{product_link}"
    )
    print("\n")
    time.sleep(3)


# Quit the browser
driver.quit()
