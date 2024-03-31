# Importing required libraries
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
from selenium.webdriver.common.action_chains import ActionChains


options = ChromeOptions()
options.set_capability("sessionName", "BStack Sample Test")

driver = webdriver.Chrome(options=options)
driver.maximize_window()


# Slow scroll function
def slow_scroll(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(0.5)


MAX_PAGE_LOAD_WAIT_TIME = 30


try:
    # Set page load timeout
    driver.set_page_load_timeout(MAX_PAGE_LOAD_WAIT_TIME)

    # Retry loading the page
    retries = 3
    for _ in range(retries):
        try:
            driver.get("https://www.flipkart.com")
            break  # If successful, exit the loop
        except (TimeoutException, WebDriverException) as e:
            print(f"Page load failed: {str(e)}. Retrying...")
    else:
        raise TimeoutException("Page load failed after multiple retries.")

    time.sleep(5)

    # Determine screen size
    window_width = driver.execute_script("return window.innerWidth")

    search_box_xpath = '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input'

    # Wait for search box to be clickable
    search_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, search_box_xpath))
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
    product_elements = driver.find_elements(By.CLASS_NAME, "_1fQZEK")
    time.sleep(2)
    # print(len(product_elements))

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
            f"Product Name:{product_name}\nDisplay Price:{display_price}\nLink to Product Details Page:{product_link}"
        )
        print("\n")
        time.sleep(2)

        # Scroll down the page
        slow_scroll(product_element)
        time.sleep(2)

except NoSuchElementException as err:
    message = "NoSuchElementException: " + str(err)
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
except NoSuchElementError as err:
    message = "NoSuchElementError: " + str(err)
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
