from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from utils.logger import get_logger


class ChromeDriver(webdriver.Chrome):

    def __init__(self, driver_path):
        self.logger = get_logger(__name__)
        try:
            options = Options()
            options.add_argument("--headless")
            service = Service(driver_path)

            super().__init__(service=service, options=options)
            self.implicitly_wait(10)
            self.wait = WebDriverWait(self, 10)
        except WebDriverException as e:
            self.logger.error(f"Error initializing WebDriver. {e}")

    def navigate(self, url):
        try:
            self.logger.info(f"navigating to {url}")
            self.get(url)
        except WebDriverException as e:
            self.logger.error(f"Error navigating to {url}. {e}")

    def find_element(self, by, value):
        try:
            return super().find_element(by, value)
        except NoSuchElementException:
            self.logger.error(f"Error finding element. {by}, {value}")
            return None

    def wait_and_get_element(self, by, value):
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return self.find_element(by, value)
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element. {by}, {value}")
            return None

    def find_elements(self, by, value):
        try:
            return super().find_elements(by, value)
        except NoSuchElementException:
            self.logger.error(f"Error finding elements. {by}, {value}")
            return []

    def wait_and_get_elements(self, by, value):
        try:
            self.wait.until(EC.visibility_of_all_elements_located((by, value)))
            return self.find_elements(by, value)
        except TimeoutException:
            self.logger.error(f"Timeout waiting for elements. {by}, {value}")
            return []

    def close(self):
        try:
            self.logger.info("Closing driver")
            self.quit()
        except WebDriverException as e:
            self.logger.error(f"Error closing the driver. {e}")