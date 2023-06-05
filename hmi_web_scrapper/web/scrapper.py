from web.driver import ChromeDriver
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import requests
import time
import os
from utils.logger import get_logger


class Scrapper:

    def __init__(self, url, driver: ChromeDriver) -> None:
        self.url = url
        self.driver = driver
        self.logger = get_logger(__name__)

    def run(self):
        self.driver.navigate(self.url)
        downloaded_files = set()
        self.logger.info("running scrapper...")
        try:
            while True:
                try:
                    
                    # refresh the page
                    self.driver.refresh()

                    csv_files = self.get_csv_files()
                    for file_name, file_url in csv_files:
                        print(file_name)
                        if file_name not in downloaded_files:
                            self.logger.info(f"New CSV file: {file_name}: {file_url}")
                            self.download_csv_file(file_name, file_url)
                            downloaded_files.add(file_name)
                    time.sleep(5)
                except Exception as e:
                    self.logger.error(f"An error occurred in run method: {e}")
                    continue
        finally:
            self.driver.close()

    def get_csv_files(self):
        # Wait for the table to load and get the table
        table: WebElement = self.driver.wait_and_get_element(By.TAG_NAME, 'table')

        # Get all rows in the table
        table_rows = table.find_elements(By.TAG_NAME, 'tr')

        # Extract CSV file links from the table
        csv_files = []
        for row in table_rows[1:]:  # Start from the second row to skip the header row
            cells: List[WebElement] = row.find_elements(By.TAG_NAME, 'td')
            if cells:
                link = cells[0].find_element(By.TAG_NAME, 'a')

                file_name = link.text
                file_url = link.get_attribute('href')
                if file_name.endswith('.CSV'):
                    csv_files.append((file_name, file_url))

        return csv_files

    def download_csv_file(self, file_name, file_url, download_path='downloads'):
        response = requests.get(file_url)
        if response.status_code == 200:
            os.makedirs(download_path, exist_ok=True)
            with open(os.path.join(download_path, file_name), 'wb') as f:
                f.write(response.content)
            self.logger.info(f"Downloaded {file_name} to {download_path}")
        else:
            self.logger.error(f"Failed to download {file_name}: status code {response.status_code}")