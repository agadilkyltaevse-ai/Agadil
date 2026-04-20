import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_BUTTONS = [
        (By.CSS_SELECTOR, "button[data-wba-header-name='Login']"),
        (By.CSS_SELECTOR, "a[data-wba-header-name='Login']"),
        (By.XPATH, "//*[contains(text(),'Войти')]"),
    ]

    PHONE_INPUTS = [
        (By.CSS_SELECTOR, "input[type='tel']"),
        (By.XPATH, "//input[contains(@placeholder,'номер')]"),
        (By.XPATH, "//input[contains(@name,'phone')]"),
    ]

    GET_CODE_BUTTONS = [
        (By.XPATH, "//button[contains(.,'Получить код')]"),
        (By.XPATH, "//button[contains(.,'получить код')]"),
    ]

    PROFILE_BUTTONS = [
        (By.CSS_SELECTOR, "a[data-wba-header-name='Profile']"),
        (By.CSS_SELECTOR, "button[data-wba-header-name='Profile']"),
        (By.XPATH, "//*[contains(text(),'Профиль')]"),
    ]

    def _find_first_visible(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            for element in elements:
                try:
                    if element.is_displayed():
                        return element
                except Exception:
                    continue
        return None

    def open_login_modal(self):
        login_button = self._find_first_visible(self.LOGIN_BUTTONS)

        if login_button is None:
            raise AssertionError("Кнопка 'Войти' не найдена.")

        try:
            login_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", login_button)

        time.sleep(2)

    def enter_phone_number(self, phone_number):
        phone_input = self._find_first_visible(self.PHONE_INPUTS)

        if phone_input is None:
            raise AssertionError("Поле ввода номера телефона не найдено.")

        try:
            phone_input.clear()
        except Exception:
            pass

        phone_input.send_keys(phone_number)
        time.sleep(1)

    def click_get_code(self):
        button = self._find_first_visible(self.GET_CODE_BUTTONS)

        if button is None:
            raise AssertionError("Кнопка 'Получить код' не найдена.")

        try:
            button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", button)

        time.sleep(2)

    def profile_button_visible(self):
        button = self._find_first_visible(self.PROFILE_BUTTONS)
        return button is not None

    def click_profile(self):
        button = self._find_first_visible(self.PROFILE_BUTTONS)

        if button is None:
            raise AssertionError("Кнопка 'Профиль' не найдена.")

        try:
            button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", button)

        time.sleep(2)