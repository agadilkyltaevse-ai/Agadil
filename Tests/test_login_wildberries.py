import time
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.regression
def test_login_request_sms_code(driver):
    home_page = HomePage(driver)
    login_page = LoginPage(driver)

    home_page.open_home_page()
    home_page.close_banner_if_present()

    login_page.open_login_modal()
    login_page.enter_phone_number("7082436521")
    login_page.click_get_code()

    print("Введи SMS-код вручную (ожидание 60 секунд)...")
    time.sleep(60)

    assert login_page.profile_button_visible(), (
        f"Авторизация не подтверждена: кнопка 'Профиль' не появилась. "
        f"Текущий URL: {driver.current_url}"
    )

    login_page.click_profile()