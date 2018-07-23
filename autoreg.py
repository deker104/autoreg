import imaplib
import base64
import html5lib
import time
import traceback
from threading import Thread
from selenium import webdriver


def register(email, password, nickname):
    server = imaplib.IMAP4_SSL('imap.yandex.ru')
    server.login(email, password)
    print('started')
    driver = webdriver.Firefox()
    driver.get('https://e-clius.com/register')

    driver.find_element_by_id('login_user').send_keys(nickname)
    driver.find_element_by_id('email_user').send_keys(email)
    driver.find_element_by_id('ob_sogl').click()
    driver.find_element_by_id('Sub').click()

    while True:
        try:
            driver.find_element_by_id('SendVerif').find_element_by_xpath('.//span').click()
            break
        except:
            traceback.print_exc()
            pass

    msgs = ['']
    while not msgs[0]:
        try:
            server.select()
            status, msgs = server.search(None, 'FROM support@e-clius.com')
            print('searched {}'.format(msgs[0]))
            time.sleep(1)
        except:
            traceback.print_exc()
            pass

    status, msg = server.fetch(msgs[0].split()[-1], '(RFC822)')
    msg = msg[0][1].splitlines()[-1]
    page_text = base64.b64decode(msg)
    page = html5lib.parse(page_text)
    code = page.findall('.//{http://www.w3.org/1999/xhtml}b')[0].text

    while True:
        try:
            el = driver.find_element_by_id('ver_code')
            break
        except:
            pass
    el.send_keys(code)

    el = driver.find_element_by_xpath('.//*[.="Проверить"]')
    el.click()

    try:
        driver.close()
    except ConnectionAbortedError:
        pass


def safe(i, f):
    def safe_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as exc:
            print(i, exc)

    return safe_f


data_s = []  # (email, password, nickname)

tasks = [Thread(target=safe(i, register), args=data) for i, data in enumerate(data_s)]

for task in tasks:
    task.start()

for task in tasks:
    task.join()
