from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        for star_value in star_values:
            star_button = self.driver.find_element(By.XPATH,
                                                   "//div[contains(text(),'{} star')]".format(star_value)
                                                   )
            star_button.click()

    def sort_by_lowest_price(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//div[@data-component="plank-sorters-bar"]'
                                            '//*[@data-sort-bar-container="sort-bar"]'
                                            '//*[@class="be1472852d"]//*[@data-id="price"]'))
        ).click()
