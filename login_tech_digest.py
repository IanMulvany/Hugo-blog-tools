from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
from simple_settings import settings
import os
import time

username = settings.TECH_DIGEST_USER
password = settings.TECH_DIGEST_PASS

def login_to_digest(driver):
    username = "test"
    form_username = driver.find_element_by_id("user_login")
    # form_password = driver.find_element_by_name("pwd")

    form_username.send_keys(username)
    # form_password.send_keys(password)

    # driver.find_element_by_name("wp-submit").click()

def navigate_to_digest(driver):
    digest_url = "https://techdigest.sagepub.com/"
    driver.get(digest_url)

driver = webdriver.Chrome()
navigate_to_digest(driver)
login_to_digest(driver)
