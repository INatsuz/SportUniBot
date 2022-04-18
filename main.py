import os
import re
from datetime import date, datetime
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from random import randint

load_dotenv()

WEEKDAY_ORDER = [("Monday", "Mon"), ("Tuesday", "Tue"), ("Wednesday", "Wed"), ("Thursday", "Thu"), ("Friday", "Fri"), ("Saturday", "Sat"), ("Sunday", "Sun")]

def login():
    # email_input = browser.find_element(By.XPATH, '//*[@id="i0116"]')
    email_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    email_input.send_keys(os.getenv("EMAIL"))

    # browser.find_element(By.ID, "idSIButton9").click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9"))).click()

    WebDriverWait(browser, 10).until(EC.staleness_of(email_input))

    password_input = browser.find_element(By.XPATH, '//*[@id="i0118"]')
    password_input.send_keys(os.getenv('PASSWORD'))

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
        weekday_index = target_date.weekday()
        today = date.today()
        delta = target_date.date() - today
        weeks_away = int(delta.days / 7) + 1 if weekday_index < today.weekday() else 0
        print(WEEKDAY_ORDER[weekday_index][1], ":", target_date.day)
        print(today)
        print("Weeks away:", weeks_away)

        regex_string = rf"{target_date.strftime('%H:%M')}\sBook\s(sports\shall|court)\s:\s{WEEKDAY_ORDER[weekday_index][1]}\s{target_date.day}.{target_date.month}."
        print("Regex: " + regex_string)

        browser.get(f'https://www.tuni.fi/sportuni/omasivu/?page=selection&lang=en&type=2&area=1&week={weeks_away}')

        link_xpath = f'//li[@class="ui-li-has-icon"]/a'
        all_link_elements = browser.find_elements(By.XPATH, link_xpath)
        for i, element in enumerate(all_link_elements):
            span_el = element.find_element(By.XPATH, "span")

            string_to_search = element.text + " : " + span_el.get_attribute("innerHTML")
            print(element.text + " : " + span_el.get_attribute("innerHTML"))

            match = re.search(regex_string, string_to_search)
            if match is not None:
                print("This is available")
                element.click()
                booking_link = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//a[contains(normalize-space(text()), "Book a court")]')))
                print(booking_link.text)
                booking_link.click()
                return True
        return False

    while try_to_book(target_date) is not True:
        sleep(randint(5, 20))
        pass


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://www.tuni.fi/sportuni/omasivu/?page=selection&lang=en&type=2&area=1&week=0")
    el = browser.find_element(By.XPATH, "//a[normalize-space(text()) = 'Sign in']")
    if el:
        browser.execute_script("arguments[0].click()", el)
        login()
        book_court()
    else:
        print("Logged in 1")

    input()