from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class InstamartScraper:

    def __init__(self):
        self.driver = None

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def open_page(self, url):
        self.driver.get(url)

        time.sleep(5)

    def get_page_source(self):
        return self.driver.page_source

    def close(self):
        if self.driver:
            self.driver.quit()