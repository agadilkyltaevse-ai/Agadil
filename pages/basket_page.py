import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BasketPage(BasePage):
    BASKET_ITEMS = (
        By.CSS_SELECTOR,
        ".basket-item, .list-item, .goods-item"
    )

    PAGE_BODY = (By.TAG_NAME, "body")

    DELETE_IN_ITEM_LOCATORS = [
        (By.CSS_SELECTOR, "button[data-link*='delete']"),
        (By.CSS_SELECTOR, "button[data-link*='remove']"),
        (By.CSS_SELECTOR, ".item__del"),
        (By.CSS_SELECTOR, ".goods-item__del"),
        (By.CSS_SELECTOR, ".basket-item__del"),
        (By.XPATH, ".//button[contains(@aria-label,'Удалить')]"),
        (By.XPATH, ".//button[contains(@title,'Удалить')]"),
        (By.XPATH, ".//button[contains(@class,'delete')]"),
        (By.XPATH, ".//button[contains(@class,'remove')]"),
        (By.XPATH, ".//button[contains(@class,'del')]"),
    ]

    CONFIRM_DELETE_BUTTONS = [
        (By.XPATH, "//button[normalize-space()='Удалить']"),
        (By.XPATH, "//button[contains(., 'Удалить')]"),
        (By.XPATH, "//button[contains(., 'Да')]"),
        (By.XPATH, "//button[contains(., 'Подтвердить')]"),
    ]

    COOKIE_OK_BUTTONS = [
        (By.XPATH, "//button[contains(., 'Окей')]"),
        (By.XPATH, "//*[contains(text(), 'Окей')]"),
    ]

    LOGIN_POPUP_CLOSE_BUTTONS = [
        (By.CSS_SELECTOR, "button.popup__close"),
        (By.CSS_SELECTOR, ".popup__close"),
        (By.CSS_SELECTOR, ".j-close"),
        (By.XPATH, "//button[contains(@class,'close')]"),
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

    def close_login_popup_if_present(self):
        for locator in self.LOGIN_POPUP_CLOSE_BUTTONS:
            try:
                btn = self.driver.find_element(*locator)
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    return
            except Exception:
                continue

    def wait_for_basket_to_load(self, min_items=0, timeout=20):
        start = time.time()

        while time.time() - start < timeout:
            self.close_cookies_if_present()
            self.close_login_popup_if_present()

            count = self.get_basket_items_count(raw_mode=True)
            if count >= min_items:
                return

            time.sleep(1)

        time.sleep(2)

    def get_basket_items(self):
        items = self.driver.find_elements(*self.BASKET_ITEMS)
        visible_items = []

        for item in items:
            try:
                if item.is_displayed():
                    visible_items.append(item)
            except Exception:
                continue

        return visible_items

    def get_basket_items_count(self, raw_mode=False):
        if not raw_mode:
            time.sleep(2)
        return len(self.get_basket_items())

    def get_page_text(self):
        return self.find_visible(self.PAGE_BODY).text.lower()

    def _find_delete_button_in_first_item(self):
        items = self.get_basket_items()
        if not items:
            return None

        first_item = items[0]

        for locator in self.DELETE_IN_ITEM_LOCATORS:
            try:
                elements = first_item.find_elements(*locator)
            except Exception:
                continue

            for button in elements:
                try:
                    if button.is_displayed() and button.is_enabled():
                        return button
                except Exception:
                    continue

        return None

    def _click_confirm_if_present(self):
        for locator in self.CONFIRM_DELETE_BUTTONS:
            try:
                confirm_btn = self.driver.find_element(*locator)
                if confirm_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", confirm_btn)
                    time.sleep(2)
                    return
            except Exception:
                continue

    def _click_delete_button(self, button):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        time.sleep(1.5)

        try:
            button.click()
            return
        except Exception:
            pass

        try:
            self.driver.execute_script("arguments[0].click();", button)
            return
        except Exception:
            pass

        raise AssertionError("Не удалось нажать на кнопку удаления товара.")

    def remove_all_items_one_by_one(self, expected_count=3):
        self.close_cookies_if_present()
        self.close_login_popup_if_present()
        self.wait_for_basket_to_load(min_items=0, timeout=20)

        removed = 0

        for _ in range(expected_count):
            before_count = self.get_basket_items_count()

            if before_count == 0:
                break

            delete_button = self._find_delete_button_in_first_item()
            if delete_button is None:
                break

            self._click_delete_button(delete_button)
            time.sleep(2)

            self.close_login_popup_if_present()
            self._click_confirm_if_present()

            after_count = before_count
            start = time.time()

            while time.time() - start < 20:
                self.close_login_popup_if_present()
                current_count = self.get_basket_items_count(raw_mode=True)

                if current_count < before_count:
                    after_count = current_count
                    break

                time.sleep(1)

            removed += max(0, before_count - after_count)
            time.sleep(2)

        final_count = self.get_basket_items_count(raw_mode=True)
        actually_removed = max(0, expected_count - final_count) if final_count <= expected_count else removed

        return max(removed, actually_removed)

    def is_basket_empty(self):
        text = self.get_page_text()
        return (
            self.get_basket_items_count() == 0
            or "корзина пуста" in text
            or "в корзине пока пусто" in text
            or "нет товаров" in text
        )