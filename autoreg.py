from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Firefox()
driver.get_cookies()
driver.get('https://e-clius.com/register')
el = driver.find_element_by_id('login_user')
el.send_keys('nickname')
el = driver.find_element_by_id('email_user')
el.send_keys('email@gmail.com')
el = driver.find_element_by_id('ob_sogl')
el.click()
el = driver.find_element_by_id('Sub')
el.click()
while True:
    try:
        el = driver.find_element_by_id('SendVerif')
    except NoSuchElementException:
        el = None
    if el:
        el = el.find_element_by_xpath('.//span')
        el.click()
        break
input('')
driver.close()