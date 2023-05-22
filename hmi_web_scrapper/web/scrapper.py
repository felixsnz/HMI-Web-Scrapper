from driver import ChromeDriver
from typing import List
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import requests
import time
import os


class Scrapper:

    def __init__(self, url, driver:webdriver.Chrome) -> None:
        self.url = url
        self.driver = driver

    def run(self):
        self.driver.get(self.url)

        downloaded_files = set()
        try:
            while True:
                try:
                    csv_files = self.get_csv_files()
                    for file_name, file_url in csv_files:
                        if file_name not in downloaded_files:
                            print(f"New CSV file: {file_name}: {file_url}")
                            self.download_csv_file(file_name, file_url)
                            downloaded_files.add(file_name)
                    time.sleep(5)
                except:
                    continue
        finally:
            self.driver.quit()


    def get_csv_files(self):
        

        # Wait for the table to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        # Get the table
        table = self.driver.find_element(By.TAG_NAME, 'table')

        # Get all rows in the table
        table_rows = table.find_elements(By.TAG_NAME, 'tr')

        # Extract CSV file links from the table
        csv_files = []
        for row in table_rows[1:]:  # Start from the second row to skip the header row
            cells:List[WebElement] = row.find_elements(By.TAG_NAME, 'td')
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
            print(f"Downloaded {file_name} to {download_path}")
        else:
            print(f"Failed to download {file_name}: status code {response.status_code}")

