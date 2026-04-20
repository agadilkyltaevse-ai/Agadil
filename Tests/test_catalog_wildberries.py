import pytest

from pages.home_page import HomePage
from pages.catalog_page import CatalogPage


@pytest.mark.regression
def test_catalog_three_paths_in_one_session(driver):
    home_page = HomePage(driver)
    catalog_page = CatalogPage(driver)

    home_page.open_home_page()
    home_page.close_banner_if_present()

    # 1 переход
    catalog_page.open_catalog_path("Обувь", "Детская", "Для девочек")

    assert catalog_page.check_category_loaded("для девочек"), (
        f"Категория 'Обувь → Детская → Для девочек' не открылась. "
        f"URL: {driver.current_url}"
    )

    # 2 переход в том же окне
    catalog_page.open_catalog_path("Детям", "Для мальчиков", "Водолазки")

    assert catalog_page.check_category_loaded("водолазки"), (
        f"Категория 'Детям → Для мальчиков → Водолазки' не открылась. "
        f"URL: {driver.current_url}"
    )

    # 3 переход в том же окне
    catalog_page.open_catalog_path("Красота", "Волосы", "Стайлинг")

    assert catalog_page.check_category_loaded("стайлинг"), (
        f"Категория 'Красота → Волосы → Стайлинг' не открылась. "
        f"URL: {driver.current_url}"
    )