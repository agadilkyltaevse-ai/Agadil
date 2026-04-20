import pytest

from pages.home_page import HomePage
from pages.filter_page import FilterPage


@pytest.mark.regression
def test_filter_laptops_by_price_range_and_delivery(driver):
    home_page = HomePage(driver)
    filter_page = FilterPage(driver)

    home_page.open_home_page()
    home_page.close_banner_if_present()
    home_page.search_for("Ноутбук")

    filter_page.open_sort_dropdown()
    filter_page.select_price_ascending()

    filter_page.open_price_filter()
    filter_page.set_price_range(20000, 35000)

    filter_page.open_delivery_filter()
    filter_page.select_delivery_up_to_3_days()

    assert filter_page.prices_in_range(20000, 35000), (
        f"Фильтр цены 20000–35000 не применился корректно. "
        f"URL: {driver.current_url}"
    )

    assert filter_page.delivery_filter_applied(), (
        f"Фильтр 'Срок доставки → до 3 дней' не применился. "
        f"URL: {driver.current_url}"
    )