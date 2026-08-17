from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time


def open_product(url):

    options = Options()

    # Keep Chrome visible while testing
    options.add_argument("--start-maximized")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    try:

        print("\nOpening Flipkart...")
        driver.get(url)

        print("Waiting for page to load...")
        time.sleep(5)

        print("\nPage title:")
        print(driver.title)

        # Give JavaScript content additional time
        time.sleep(3)

        html = driver.page_source

        print(
            f"\nHTML captured: {len(html)} characters"
        )

        return html

    except Exception as e:

        print("\nSelenium error:")
        print(str(e))

        return None

    finally:

        print("\nClosing browser...")
        driver.quit()