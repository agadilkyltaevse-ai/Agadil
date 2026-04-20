import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.basket_page import BasketPage


@pytest.mark.regression
def test_basket_add_and_remove_three_products(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    basket_page = BasketPage(driver)

    driver.get("https://www.wildberries.ru/lk/basket?selectedTabId=main")
    basket_page.wait_for_basket_to_load(min_items=0, timeout=20)

    if not basket_page.is_basket_empty():
        basket_page.remove_all_items_one_by_one(expected_count=10)

    home_page.open_home_page()
    home_page.close_banner_if_present()
    home_page.search_for("органайзер")

    product_links = home_page.get_product_hrefs_with_scroll(needed_count=3)

    for link in product_links:
        driver.get(link)
        product_page.add_to_basket()

    driver.get("https://www.wildberries.ru/lk/basket?selectedTabId=main")
    basket_page.wait_for_basket_to_load(min_items=3, timeout=25)

    items_count = basket_page.get_basket_items_count()

    assert items_count == 3, (
        f"Ожидалось 3 товара в корзине, найдено {items_count}. "
        f"URL: {driver.current_url}"
    )

    removed_count = basket_page.remove_all_items_one_by_one(expected_count=3)

    assert removed_count == 3, (
        f"Ожидалось удалить 3 товара, но удалено {removed_count}. "
        f"URL: {driver.current_url}"
    )

    assert basket_page.is_basket_empty(), (
        f"После удаления корзина не стала пустой. "
        f"Товаров осталось: {basket_page.get_basket_items_count()}. "
        f"URL: {driver.current_url}"
    )