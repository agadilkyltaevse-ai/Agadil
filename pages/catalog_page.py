import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage


class CatalogPage(BasePage):
    PAGE_BODY = (By.TAG_NAME, "body")

    BURGER_BUTTONS = [
        (By.CSS_SELECTOR, "button.nav-element__burger"),
        (By.CSS_SELECTOR, "button.j-menu-burger-btn"),
        (By.CSS_SELECTOR, ".nav-element__burger"),
        (By.CSS_SELECTOR, ".menu-burger"),
        (By.XPATH, "//button[contains(@class,'burger')]"),
    ]

    def open_burger_menu(self):
        for locator in self.BURGER_BUTTONS:
            try:
                burger = self.wait.until(lambda d: d.find_element(*locator))
                self.wait.until(lambda d: burger.is_displayed() and burger.is_enabled())

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", burger
                )
                time.sleep(1)

                try:
                    burger.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", burger)

                time.sleep(2)
                return

            except Exception:
                continue

        raise AssertionError("Не удалось нажать кнопку бургер-меню.")

    def _find_visible_element_by_text(self, text):
        xpath_variants = [
            f"//a[contains(., '{text}')]",
            f"//button[contains(., '{text}')]",
            f"//span[contains(., '{text}')]",
            f"//*[contains(text(), '{text}')]",
        ]

        for xpath in xpath_variants:
            elements = self.driver.find_elements(By.XPATH, xpath)

            for element in elements:
                try:
                    if element.is_displayed():
                        return element
                except Exception:
                    continue

        return None

    def hover_menu(self, text):
        element = self._find_visible_element_by_text(text)

        if element is None:
            raise AssertionError(f"Не найден пункт '{text}'")

        ActionChains(self.driver).move_to_element(element).pause(1).perform()
        time.sleep(2)

    def click_menu(self, text):
        element = self._find_visible_element_by_text(text)

        if element is None:
            raise AssertionError(f"Не найден пункт '{text}'")

        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

        time.sleep(2)

    def open_catalog_path(self, level1, level2, level3):
        self.open_burger_menu()
        self.hover_menu(level1)
        self.click_menu(level2)
        self.click_menu(level3)

    def get_page_text(self):
        return self.find_visible(self.PAGE_BODY).text.lower()

    def check_category_loaded(self, keyword):
        return keyword.lower() in self.get_page_text()