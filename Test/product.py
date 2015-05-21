__author__ = 'yanaor'

from base import BasePage
from base import InvalidPageException


class ProductPage(BasePage):
    _product_view_locator = 'div.product-view'
    _product_name_locator = 'div.product-namespan'
    _product_description_locator = 'div.tab-contentdiv.std'
    _product_stock_status_locator = 'p.availabilityspan.value'
    _product_price_locator = 'span.price'

    def __init__(self, driver):
        super(ProductPage, self).__init__(driver)

    @property
    def name(self):
        return self.driver.find_element_by_css_selector(self._product_name_locator).text.strip()

    @property
    def description(self):
        return self.driver.find_element_by_css_selector(self._product_description_locator).text.strip()

    @property
    def stock_status(self):
        return self.driver.find_element_by_css_selector(self._product_stock_status_locator).text.strip()

    @property
    def price(self):
        return self.driver.find_element_by_css_selector(self._product_price_locator).text.strip()

    def _validate_page(self, driver):
        try:
            driver.find_element_by_css_selector(self._product_view_locator)
        except:
            raise InvalidPageException('Product page not loaded')