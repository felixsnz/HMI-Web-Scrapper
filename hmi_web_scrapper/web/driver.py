from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


class ChromeDriver(webdriver.Chrome):

    def __init__(self, driver_path):
        try:
            options = Options()
            options.add_argument("--headless")
            service = Service(driver_path)

            # Replace 'chromedriver' with the path to your ChromeDriver executable
            super().__init__(service=service, options=options)
            self.implicitly_wait(10)
        except WebDriverException as e:
            print(f"Error initializing WebDriver. {e}")

    def navigate(self, url):
        try:
            self.get(url)
        except WebDriverException as e:
            print(f"Error navigating to {url}. {e}")

    def find_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except WebDriverException as e:
            print(f"Error finding element. {e}")

    def close(self):
        self.quit()