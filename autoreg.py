from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://e-clius.com/register')
el = driver.find_element_by_id('login_user')
el.send_keys('nickname')
el = driver.find_element_by_id('email_user')
el.send_keys('email@gmail.com')
el = driver.find_element_by_id('ob_sogl')
el.click()
el = driver.find_element_by_id('Sub')
el.click()
input('')
driver.close()