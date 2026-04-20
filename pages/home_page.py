import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://www.wildberries.ru/"

    SEARCH_INPUT = (By.ID, "searchInput")
    PAGE_BODY = (By.TAG_NAME, "body")

    CLOSE_BANNER_BUTTONS = [
        (By.CSS_SELECTOR, "button.popup__close"),
        (By.CSS_SELECTOR, ".popup__close"),
        (By.CSS_SELECTOR, ".j-close"),
        (By.CSS_SELECTOR, ".cookies__btn-close"),
    ]

    PRODUCT_LINKS = [
        (By.CSS_SELECTOR, "a.product-card__link"),
        (By.CSS_SELECTOR, "a.j-card-link"),
        (By.CSS_SELECTOR, ".product-card a[href*='/catalog/']"),
    ]

    BASKET_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-wba-header-name='Cart'], a[href*='/lk/basket'], .navbar-pc__link--basket"
    )

    def open_home_page(self):
        self.open(self.URL)
        self.find_visible(self.PAGE_BODY)

    def close_banner_if_present(self):
        for locator in self.CLOSE_BANNER_BUTTONS:
            try:
                self.find_clickable(locator).click()
                time.sleep(1)
                return
            except TimeoutException:
                continue

    def search_for(self, text: str):
        search_input = self.find_visible(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)
        self.wait.until(
            lambda d: "search" in d.current_url.lower() or "catalog" in d.current_url.lower()
        )
        time.sleep(2)

    def _collect_product_hrefs(self):
        hrefs = []

        for locator in self.PRODUCT_LINKS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                href = el.get_attribute("href")
                if href and "/catalog/" in href and href not in hrefs:
                    hrefs.append(href)

        return hrefs

    def get_product_hrefs_with_scroll(self, needed_count=3, max_scrolls=8, step=1200):
        hrefs = []

        for _ in range(max_scrolls):
            current_hrefs = self._collect_product_hrefs()

            for href in current_hrefs:
                if href not in hrefs:
                    hrefs.append(href)

            if len(hrefs) >= needed_count:
                return hrefs[:needed_count]

            self.scroll_by(step)
            time.sleep(2)

        if len(hrefs) < needed_count:
            raise AssertionError(
                f"Не удалось найти {needed_count} товаров. Найдено только {len(hrefs)}."
            )

        return hrefs[:needed_count]

    def open_basket(self):
        self.find_clickable(self.BASKET_BUTTON).click()
        time.sleep(2)