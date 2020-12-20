import argparse
import datetime
import logging
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

FIT4LESS_GYMMANAGER_LOGIN_URL = "https://myfit4less.gymmanager.com/portal/login.asp"

LOGIN_EMAIL = "hardikvala24@gmail.com"
LOGIN_PASSWORD = "bL3t-7here-83-L"

# Number of days into the future to book a workout slot. Fit4Less allows booking 
# a maximum of 2 days in advance. But bookings become available at midnight, ET,
# and this script will run at 9 pm, PT, so necessarily, the value here is 3
# days.

BOOKING_TIMES = ["10:00 AM", "11:30 AM", "9:30 AM", "11:00 AM"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--chromedriver_path', type=str,
                    help="Path to chromedriver executable.")
parser.add_argument('--num_future_booking_days', type=int, default=2,
                    help="Number of days into the future to book a workout slot.")

def main():
    ## Parse commandline arguments ##

    args = parser.parse_args()

    ## Initialize web driver ## 

    chrome_options = Options()
    # Running in headless mode results in,
    # selenium.common.exceptions.ElementClickInterceptedException: Message:
    # element click intercepted: Element <div id="loginButton" class="button">...</div>
    # is not clickable at point (400, 579). Other element would receive the click:
    # <div class="footer">...</div>
    # chrome_options.add_argument("--headless")
    
    if args.chromedriver_path:
        with webdriver.Chrome(executable_path=args.chromedriver_path, options=chrome_options) as driver:
            book_slot(driver, args.num_future_booking_days)
    else:
        with webdriver.Chrome(options=chrome_options) as driver:
            book_slot(driver, args.num_future_booking_days)

def book_slot(driver, num_future_booking_days):
    ## Load Fit4Less gymmanager web page ##
    logging.info("Visiting %s..." % FIT4LESS_GYMMANAGER_LOGIN_URL)

    driver.get(FIT4LESS_GYMMANAGER_LOGIN_URL) 

    time.sleep(1)

    ## Login ##
    logging.info("Logging in...")
    
    email_field = driver.find_element_by_name("emailaddress")
    password_field = driver.find_element_by_name("password")

    action = ActionChains(driver)
    action.click(on_element=email_field)
    action.send_keys(LOGIN_EMAIL)
    action.click(on_element=password_field)
    action.send_keys(LOGIN_PASSWORD)
    action.perform()

    login_button = driver.find_element_by_id("loginButton")
    login_button.click()

    time.sleep(1)

    ## Select latest booking date ##
    logging.info("Select booking date...")
    
    try:
        select_day_button = driver.find_element_by_id("btn_date_select")
    except NoSuchElementException:
        logging.error("Cannot select booking date")
        sys.exit(1)

    select_day_button.click() 

    time.sleep(1)

    now = datetime.datetime.now()
    latest_booking_date = now + datetime.timedelta(days=num_future_booking_days)

    logging.info("Booking date: %s" % latest_booking_date.strftime('%Y.%m.%d'))

    booking_date_id = latest_booking_date.strftime('date_%Y-%m-%d')
    latest_booking_date_button = driver.find_element_by_id(booking_date_id)
    latest_booking_date_button.click() 

    time.sleep(1)

    ## Find time slots ##
    logging.info("Finding time slots...")

    try:
        time_slots = driver.find_elements_by_xpath("//div[@class=\"available-slots\"]/div[@class=\"time-slot\"]")
    except NoSuchElementException:
        logging.error("No time slots found")
        sys.exit(1)    

    if len(time_slots) == 0:
        logging.error("No time slots found")
        sys.exit(1)    

    ## Book time slot ##
    logging.info("Booking time slot...")

    for booking_time in BOOKING_TIMES: 
        for time_slot in time_slots:
            if time_slot.get_attribute('data-slottime').endswith(booking_time):
                time_slot.click()

                time.sleep(1)
                
                time_slot_dialog_book_yes_button = driver.find_element_by_id("dialog_book_yes")
                time_slot_dialog_book_yes_button.click()

                logging.info("Booked time slot on %s at %s" % (latest_booking_date.strftime('%Y.%m.%d'), booking_time))

                sys.exit(0)
        logging.warning("No time slot found for %s", booking_time)



if __name__ == "__main__":
    main()

