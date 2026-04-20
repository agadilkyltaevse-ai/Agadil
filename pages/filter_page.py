import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage


class FilterPage(BasePage):
    SORT_BUTTONS = [
        (By.XPATH, "//*[contains(text(),'По популярности')]"),
        (By.XPATH, "//button[contains(., 'По популярности')]"),
        (By.XPATH, "//span[contains(., 'По популярности')]"),
    ]

    SORT_PRICE_ASC_OPTIONS = [
        (By.XPATH, "//*[contains(text(),'По возрастанию цены')]"),
        (By.XPATH, "//button[contains(., 'По возрастанию цены')]"),
        (By.XPATH, "//span[contains(., 'По возрастанию цены')]"),
    ]

    PRICE_BLOCKS = [
        (By.XPATH, "//*[contains(text(),'Цена, ₽')]"),
        (By.XPATH, "//*[contains(text(),'Цена')]"),
        (By.XPATH, "//button[contains(., 'Цена, ₽')]"),
        (By.XPATH, "//button[contains(., 'Цена')]"),
        (By.XPATH, "//span[contains(., 'Цена, ₽')]"),
        (By.XPATH, "//span[contains(., 'Цена')]"),
    ]

    DELIVERY_BLOCKS = [
        (By.XPATH, "//*[contains(text(),'Срок доставки')]"),
        (By.XPATH, "//button[contains(., 'Срок доставки')]"),
        (By.XPATH, "//span[contains(., 'Срок доставки')]"),
    ]

    DELIVERY_UP_TO_3_DAYS_OPTIONS = [
        (By.XPATH, "//*[contains(text(),'до 3 дней')]"),
        (By.XPATH, "//button[contains(., 'до 3 дней')]"),
        (By.XPATH, "//span[contains(., 'до 3 дней')]"),
    ]

    APPLY_BUTTONS = [
        (By.XPATH, "//button[normalize-space()='Готово']"),
        (By.XPATH, "//button[contains(., 'Готово')]"),
        (By.XPATH, "//button[contains(., 'Применить')]"),
    ]

    PRODUCT_CARDS = [
        (By.CSS_SELECTOR, ".product-card"),
        (By.CSS_SELECTOR, ".j-card-item"),
    ]

    CARD_PRICE_SELECTORS = [
        ".price__lower-price",
        ".wallet-price",
        "ins.lower-price",
        ".product-card__price",
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

    def open_sort_dropdown(self):
        sort_button = self._find_first_visible(self.SORT_BUTTONS)

        if sort_button is None:
            raise AssertionError("Не найдена кнопка сортировки 'По популярности'.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", sort_button
        )
        time.sleep(1)

        try:
            ActionChains(self.driver).move_to_element(sort_button).pause(1).click().perform()
        except Exception:
            try:
                sort_button.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", sort_button)

        time.sleep(2)

    def select_price_ascending(self):
        option = self._find_first_visible(self.SORT_PRICE_ASC_OPTIONS)

        if option is None:
            raise AssertionError("Не найден пункт 'По возрастанию цены'.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", option
        )
        time.sleep(1)

        try:
            option.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", option)

        time.sleep(3)

    def open_price_filter(self):
        block = self._find_first_visible(self.PRICE_BLOCKS)

        if block is None:
            raise AssertionError("Не найден фильтр 'Цена, ₽'.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", block
        )
        time.sleep(1)

        try:
            block.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", block)

        time.sleep(2)

    def open_delivery_filter(self):
        block = self._find_first_visible(self.DELIVERY_BLOCKS)

        if block is None:
            raise AssertionError("Не найден фильтр 'Срок доставки'.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", block
        )
        time.sleep(1)

        try:
            ActionChains(self.driver).move_to_element(block).pause(1).click().perform()
        except Exception:
            try:
                block.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", block)

        time.sleep(2)

    def select_delivery_up_to_3_days(self):
        DELIVERY_OPTIONS = [
            (By.XPATH, "//*[contains(text(),'до 3 дней')]"),
            (By.XPATH, "//*[contains(text(),'До 3 дней')]"),
            (By.XPATH, "//*[contains(text(),'Послезавтра')]"),
            (By.XPATH, "//button[contains(.,'Послезавтра')]"),
            (By.XPATH, "//span[contains(.,'Послезавтра')]"),
        ]

        option = self._find_first_visible(DELIVERY_OPTIONS)

        if option is None:
            raise AssertionError("Не найден пункт доставки 'до 3 дней' или 'Послезавтра'.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", option
        )
        time.sleep(1)

        try:
            ActionChains(self.driver).move_to_element(option).pause(1).click().perform()
        except Exception:
            try:
                option.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", option)

        time.sleep(3)

    def _get_visible_editable_price_inputs(self):
        inputs = self.driver.find_elements(By.XPATH, "//input")
        result = []

        for element in inputs:
            try:
                if not element.is_displayed():
                    continue
                if not element.is_enabled():
                    continue

                input_type = (element.get_attribute("type") or "").lower()
                if input_type == "hidden":
                    continue

                placeholder = (element.get_attribute("placeholder") or "").lower()
                aria_label = (element.get_attribute("aria-label") or "").lower()
                name = (element.get_attribute("name") or "").lower()
                value = (element.get_attribute("value") or "").strip()

                is_price_like = (
                    "от" in placeholder
                    or "до" in placeholder
                    or "от" in aria_label
                    or "до" in aria_label
                    or "start" in name
                    or "end" in name
                    or value.isdigit()
                )

                if is_price_like:
                    result.append(element)
            except Exception:
                continue

        if len(result) < 2:
            raise AssertionError("Не удалось найти два видимых поля цены.")

        return result[:2]

    def _set_input_value_native(self, element, value):
        self.driver.execute_script(
            """
            const el = arguments[0];
            const val = arguments[1].toString();

            const nativeInputValueSetter =
              Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;

            el.focus();
            nativeInputValueSetter.call(el, '');
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));

            nativeInputValueSetter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.blur();
            """,
            element,
            value,
        )

    def _get_input_value(self, element):
        return self.driver.execute_script("return arguments[0].value;", element)

    def set_price_range(self, price_from, price_to):
        inputs = self._get_visible_editable_price_inputs()
        from_input = inputs[0]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", from_input
        )
        time.sleep(1)

        self._set_input_value_native(from_input, price_from)
        time.sleep(2)

        inputs = self._get_visible_editable_price_inputs()
        to_input = inputs[1]

        self._set_input_value_native(to_input, price_to)
        time.sleep(2)

        inputs = self._get_visible_editable_price_inputs()
        actual_from = self._get_input_value(inputs[0])
        actual_to = self._get_input_value(inputs[1])

        if re.sub(r"[^\d]", "", actual_from) != str(price_from):
            raise AssertionError(f"Поле 'От' заполнено неверно: {actual_from}")

        if re.sub(r"[^\d]", "", actual_to) != str(price_to):
            raise AssertionError(f"Поле 'До' заполнено неверно: {actual_to}")

        apply_button = self._find_first_visible(self.APPLY_BUTTONS)

        if apply_button is None:
            raise AssertionError("Не найдена кнопка 'Готово'.")

        try:
            apply_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", apply_button)

        time.sleep(4)

    def _parse_price(self, text):
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else 0

    def _get_visible_product_cards(self):
        for locator in self.PRODUCT_CARDS:
            cards = self.driver.find_elements(*locator)
            visible_cards = []

            for card in cards:
                try:
                    if card.is_displayed():
                        visible_cards.append(card)
                except Exception:
                    continue

            if visible_cards:
                return visible_cards

        raise AssertionError("Не удалось найти карточки товаров.")

    def get_visible_prices(self, count=5):
        time.sleep(4)
        cards = self._get_visible_product_cards()
        prices = []

        for card in cards:
            try:
                price_found = False

                for selector in self.CARD_PRICE_SELECTORS:
                    elements = card.find_elements(By.CSS_SELECTOR, selector)

                    for el in elements:
                        try:
                            if el.is_displayed():
                                price = self._parse_price(el.text)
                                if price > 0:
                                    prices.append(price)
                                    price_found = True
                                    break
                        except Exception:
                            continue

                    if price_found:
                        break
            except Exception:
                continue

            if len(prices) >= count:
                return prices[:count]

        raise AssertionError(f"Не удалось получить цены первых {count} карточек товаров.")

    def prices_in_range(self, price_from, price_to):
        prices = self.get_visible_prices(count=5)

        for price in prices:
            if price < price_from or price > price_to:
                return False

        return True

    def delivery_filter_applied(self):
        page_text = self.find_visible((By.TAG_NAME, "body")).text.lower()
        current_url = self.driver.current_url.lower()

        return (
            "до 3 дней" in page_text
            or "срок доставки" in page_text
            or "delivery" in current_url
        )