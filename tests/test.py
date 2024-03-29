import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException


# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability("sessionName", "BStack Sample Test")
driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.maximize_window()

MAX_PAGE_LOAD_WAIT_TIME = 60


def find_element_with_retry(driver, by, value, retries=5, delay=20):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print("Element not found. Retrying...")
    # If element is not found after all retries, raise TimeoutException
    raise TimeoutException(
        f"Element with {by}={value} not found after {retries} retries"
    )


try:
    # Set page load timeout
    # driver.set_page_load_timeout(MAX_PAGE_LOAD_WAIT_TIME)

    # Retry loading the page
    retries = 5
    for _ in range(retries):
        try:
            driver.get("https://www.flipkart.com")
            break  # If successful, exit the loop
        except (TimeoutException, WebDriverException) as e:
            print(f"Page load failed: {str(e)}. Retrying...")
    else:
        raise TimeoutException("Page load failed after multiple retries.")

    time.sleep(5)
    # Use WebDriverWait instead of time.sleep
    # search_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
    # Wait for search box to be clickable
    # Determine screen size
    window_width = driver.execute_script("return window.innerWidth")
    if window_width >= 768:
        search_box_xpath = '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input'
    else:
        search_box_xpath = '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div[2]'

    # Wait for search box to be clickable
    search_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, search_box_xpath))
    )

    if window_width >= 768:
        print("HELLO")
    else:
        search_box.click()
        search_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "input-searchsearchpage-input"))
        )

    search_box.send_keys("Samsung Galaxy S10")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Click on "Mobiles" in categories
    mobiles_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="container"]/div/div[3]/div[1]/div[1]/div/div[1]/div/div/section/div[3]/div/a',
            )
        )
    )
    mobiles_category.click()
    time.sleep(3)

    # Apply filters
    brand_filter_checkbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="container"]/div/div[3]/div[1]/div[1]/div/div[1]/div/section[3]/div[2]/div/div/div/label/div[1]',
            )
        )
    )
    brand_filter_checkbox.click()
    time.sleep(3)

    flipkart_assured_filter = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="container"]/div/div[3]/div/div[1]/div/div[1]/div/section[4]/label/div[1]',
            )
        )
    )
    flipkart_assured_filter.click()
    time.sleep(3)

    # Sort by price high to low
    sort_dropdown = WebDriverWait(driver, 20).until(
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
    product_elements = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "_1fQZEK"))
    )
    time.sleep(3)

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
            f"Product name: {product_name}\nDisplay price: {display_price}\nMore Details: {product_link}\n"
        )
        time.sleep(2)

except NoSuchElementException as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
except TimeoutException as err:
    message = "TimeoutException: " + str(err)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
except ElementNotInteractableException as err:
    message = "ElementNotInteractableException: " + str(err)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
except Exception as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
finally:
    # Stop the driver
    driver.quit()
