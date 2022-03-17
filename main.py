from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from datetime import date, datetime

WEEKDAY_ORDER = [("Saturday", "Sat"), ("Sunday", "Sun"), ("Monday", "Mon"), ("Tuesday", "Tue"), ("Wednesday", "Wed"), ("Thursday", "Thu"), ("Friday", "Fri")]


def login():
    email_input = browser.find_element(By.XPATH, '//*[@id="i0116"]')
    email_input.send_keys(input("Insert your email: "))

    browser.find_element(By.ID, "idSIButton9").click()

    WebDriverWait(browser, 10).until(EC.staleness_of(email_input))

    password_input = browser.find_element(By.XPATH, '//*[@id="i0118"]')
    password_input.send_keys(input("Insert password: "))

    browser.find_element(By.ID, "idSIButton9").click()

    WebDriverWait(browser, 10).until(EC.staleness_of(password_input))

    auth_code_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'idTxtBx_SAOTCC_OTC')))
    auth_code_input.send_keys(input("Auth Code: "))
    browser.find_element(By.XPATH, '//*[@id="idSubmit_SAOTCC_Continue"]').click()

    stay_signed_in_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]')))
    stay_signed_in_btn.click()


def book_court():
    line = input("Day and time (eg. 18.3. 10:00)")
    day, time = line.split(" ")
    formatted_date_string = day.replace(".", "/") + "/22" + " " + time
    print(formatted_date_string)
    target_date = datetime.strptime(formatted_date_string, "%d/%m/%y %H:%M")
    print(target_date)

    def try_to_book(target_date):
        today = date.today()
        print(today)
        delta = target_date.date() - today
        print(delta.days)
        print((target_date.weekday() + 2) % 7)
        print((today.weekday() + 2) % 7)
        print("Weeks away:", int(delta.days / 7) + 1 if (target_date.weekday() + 2) % 7 < (today.weekday() + 2) % 7 else 0)

    try_to_book(target_date)


if __name__ == '__main__':

    book_court()

    # chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    #
    # browser = webdriver.Chrome(options=chrome_options)
    # browser.get("https://www.tuni.fi/sportuni/omasivu/?page=selection&lang=en&type=2&area=1&week=0")
    # el = browser.find_element(By.XPATH, "//a[normalize-space(text()) = 'Sign in']")
    # if el:
    #     browser.execute_script("arguments[0].click()", el)
    #     login()
    # else:
    #     print("Logged in 1")

    input()