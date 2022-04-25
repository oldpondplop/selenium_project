import os
from datetime import datetime
from selenium import webdriver
import booking.constans as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from booking.booking_filtration import BookingFiltration
from selenium.webdriver.support import expected_conditions as EC


class Booking(webdriver.Chrome):
    def __init__(self, teardown=False, driver_path= const.DRIVER_PATH):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def accept_cookies(self):
        WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()
        selected_currency_element = self.find_element_by_css_selector(
            'a[data-modal-header-async-url-param*="selected_currency=%s"]' % currency
        )
        selected_currency_element.click()

    def select_place_to_go(self, place=None):
        search_field = self.find_element_by_id("ss")
        search_field.clear()
        search_field.send_keys(place)

        first_result = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )

        first_result.click()

    def select_dates(self, start_date, end_date):
        check_in_element = self.find_element_by_css_selector(
            f'td[data-date="{start_date}"]'
        )
        self.execute_script("arguments[0].click();", check_in_element)

        check_out_element = self.find_element_by_css_selector(
            f'td[data-date="{end_date}"]'
        )
        self.execute_script("arguments[0].click();", check_out_element)

    @staticmethod
    def get_date(start_date, end_date):
        current_date = datetime.now()
        checkin_date = datetime.strptime(start_date, "%Y-%m-%d")
        checkout_date = datetime.strptime(end_date, "%Y-%m-%d")
        checkin_diff = (checkin_date.month - current_date.month) % 12
        checkout_diff = (checkout_date.month - checkin_date.month) % 12
        return checkin_diff, checkout_diff

    def select_dates(self, start_date, end_date):
        checkin_diff, checkout_diff = self.get_date(start_date, end_date)
        next_month = self.find_element(By.XPATH,
                                       '//div[@class="bui-calendar__control bui-calendar__control--next"]'
                                       )
        for _ in range(checkin_diff - 1):
            next_month.click()
        checkin_element = self.find_element(By.XPATH, fr'//td[@data-date="{start_date}"]')
        self.execute_script("arguments[0].click();", checkin_element)
        for _ in range(checkout_diff):
            next_month.click()
        checkout_element = self.find_element(By.XPATH, fr'//td[@data-date="{end_date}"]')
        self.execute_script("arguments[0].click();", checkout_element)

    def select_group(self, group, count):

        while True:
            decrease_element = self.find_element(By.CSS_SELECTOR,
                                                 fr'button[aria-label="Decrease number of {group}"]'
                                                 )
            decrease_element.click()

            if group == 'Rooms':
                value_element = self.find_element(By.ID, f'no_{group.lower()}')
            else:
                value_element = self.find_element(By.ID, f'group_{group.lower()}')
            default_value = value_element.get_attribute('value')

            if int(default_value) == 1 or int(default_value) == 0:
                break
        
        increase_element = self.find_element(By.CSS_SELECTOR,
                                             fr'button[aria-label="Increase number of {group}"]'
                                             )
        for _ in range(count - 1):
            increase_element.click()

    def rooms_and_occupancy(self, rooms, adults, children):
        select_element = self.find_element(By.ID, 'xp__guests__toggle')
        select_element.click()

        self.select_group(group='Adults', count=adults)
        self.select_group(group='Children', count=children)
        self.select_group(group='Rooms', count=rooms)

    def search(self):
        self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    def apply_filtration(self, *star_ratings):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(*star_ratings)
        filtration.sort_by_lowest_price()
