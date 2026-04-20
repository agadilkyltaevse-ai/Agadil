import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME_LOCATORS = [
        (By.CSS_SELECTOR, "h1"),
        (By.CSS_SELECTOR, ".product-page__title"),
        (By.CSS_SELECTOR, ".goods-name"),
    ]

    PAGE_BODY = (By.TAG_NAME, "body")

    ADD_TO_BASKET_BUTTONS = [
        (By.XPATH, "//button[normalize-space()='Добавить в корзину']"),
        (By.XPATH, "//button[contains(., 'Добавить в корзину')]"),
        (By.XPATH, "//a[contains(., 'Добавить в корзину')]"),
        (By.CSS_SELECTOR, ".order__button"),
        (By.CSS_SELECTOR, ".product-page__order button"),
        (By.CSS_SELECTOR, ".sidebar__sticky-wrap button"),
    ]

    COOKIE_OK_BUTTONS = [
        (By.XPATH, "//button[contains(., 'Окей')]"),
        (By.XPATH, "//*[contains(text(), 'Окей')]"),
    ]

    def close_cookies_if_present(self):
        for locator in self.COOKIE_OK_BUTTONS:
            try:
                btn = self.driver.find_element(*locator)
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    return
            except Exception:
                continue

    def get_product_name(self):
        time.sleep(2)

        for locator in self.PRODUCT_NAME_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for element in elements:
                text = element.text.strip().lower()
                if text:
                    return text

        return ""

    def get_page_text(self):
        return self.find_visible(self.PAGE_BODY).text.lower()

    def product_matches_search(self, search_text: str) -> bool:
        search_words = [word.lower() for word in search_text.split() if word.strip()]
        product_name = self.get_product_name()

        if any(word in product_name for word in search_words):
            return True

        page_text = self.get_page_text()
        return any(word in page_text for word in search_words)

    def add_to_basket(self):
        self.close_cookies_if_present()
        time.sleep(2)

        for locator in self.ADD_TO_BASKET_BUTTONS:
            try:
                button = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                return
            except Exception:
                continue

        raise AssertionError("Кнопка 'Добавить в корзину' не найдена или не нажимается.")