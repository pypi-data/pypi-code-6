from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


SIGNIN_URL = "https://accounts.coursera.org/signin"
TIMEOUT = 60

def signin(web, username, password):
    """
    Sign in with `username` and `password`
    Returns cookies after signed-in
    """
    web.get(SIGNIN_URL)

    email = wait(web, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "signin-email")))
    email.send_keys(username)

    pwd = web.find_element_by_id('signin-password')
    pwd.send_keys(password)

    btn = web.find_element_by_class_name('coursera-signin-button')
    btn.click()

    wait(web, TIMEOUT).until(EC.title_contains('Your Courses'))

    return web.get_cookies()


def get_cookie(username, password, proxy):
    """
    Launch a chrome to get cookies
    """
    chromeopts = ChromeOptions()
    if proxy:
        chromeopts.add_argument('--proxy-server=%s' % proxy)

    web = Chrome(chrome_options=chromeopts)
    try:
        return signin(web, username, password)
    finally:
        web.quit()


def format_cookie(cookie):
    return ' '.join(['%s=%s;' % (c['name'], c['value']) for c in cookie])
