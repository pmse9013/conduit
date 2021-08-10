import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from webdriver_manager.chrome import ChromeDriverManager



def sign_in(driver):
    driver.find_element_by_xpath("//a[@href='#/login']").click()
    element = WebDriverWait(
        driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Sign in')]"))
    )
    driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys("papp.emese9013+3@gmail.com")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Jelszó123")
    driver.find_element_by_xpath("//button[contains(text(),'Sign in')]").click()
    element = WebDriverWait(
        driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "// a[contains(text(), 'Your Feed')]"))
    )
