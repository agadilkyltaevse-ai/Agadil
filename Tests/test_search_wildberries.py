import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.basket_page import BasketPage


@pytest.mark.smoke
@pytest.mark.parametrize(
    "search_text",
    [
        "ноутбук",
        "кроссовки",
        "рюкзак",
        "футболка",
        "наушники",
    ],
)
def test_search_opens_product_and_matches_query(driver, search_text):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)

    home_page.open_home_page()
    home_page.close_banner_if_present()
    home_page.search_for(search_text)

    product_links = home_page.get_product_hrefs_with_scroll(needed_count=1)
    driver.get(product_links[0])

    product_name = product_page.get_product_name()

    assert product_page.product_matches_search(search_text), (
        f"Открытый товар не соответствует поисковому запросу '{search_text}'. "
        f"Название товара: '{product_name}'. "
        f"URL: {driver.current_url}"
    )


@pytest.mark.regression
def test_add_and_remove_three_products_in_same_session(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    basket_page = BasketPage(driver)

    home_page.open_home_page()
    home_page.close_banner_if_present()
    home_page.search_for("органайзер")

    product_links = home_page.get_product_hrefs_with_scroll(needed_count=3)

    for link in product_links:
        driver.get(link)
        product_page.add_to_basket()

    driver.get("https://www.wildberries.ru/lk/basket?selectedTabId=main")

    items_count = basket_page.get_basket_items_count()

    assert items_count == 3, (
        f"Ожидалось 3 товара в корзине после добавления, но найдено {items_count}. "
        f"URL: {driver.current_url}"
    )

    removed_count = basket_page.remove_all_items_one_by_one(expected_count=3)

    assert removed_count == 3, (
        f"Ожидалось удалить 3 товара из корзины, но удалено {removed_count}. "
        f"URL: {driver.current_url}"
    )

    assert basket_page.is_basket_empty(), (
        f"После удаления корзина не стала пустой. "
        f"Товаров осталось: {basket_page.get_basket_items_count()}. "
        f"URL: {driver.current_url}"
    )