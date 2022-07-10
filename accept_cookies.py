from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def load_and_accept_cookies(URL = None, switch_to_frame = None, button_id = None) -> webdriver.Chrome:
    if URL == None or switch_to_frame == None or button_id == None:
        print()
        print("################################################")
        print("load_and_accept_cookies ERROR. Please add value!")
        print("################################################")
        print()
    else:
        driver = webdriver.Chrome()
        driver.get(URL)
        time.sleep(3)
        driver.switch_to.frame(switch_to_frame)
        accept_cookies_button = driver.find_element(By.ID, button_id)
        accept_cookies_button.click()
        time.sleep(1)

        return driver

    