from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


class Browser:


    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def perform_google_search(self, term):
        self.driver.get("https://www.google.com/search?q=" + term)

    def accept_google_cookies(self):
        time.sleep(0.5)
        btn = self.driver.find_element(By.ID, "L2AGLb")
        btn.click()

    def get_all_google_result_urls(self):
        time.sleep(0.5)
        webelements_ls = self.driver.find_elements(By.CLASS_NAME, "yuRUbf")
        return webelements_ls
        #urls = [elm. for elm in webelements_ls]
    
    def visit_page(self, url):
        self.driver.get(url)