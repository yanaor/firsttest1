__author__ = 'yanaor'
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class HomePageTest1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a new Firefox session """
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()
        # navigate to the application home page """
        cls.driver.get("http://demo.magentocommerce.com/")

    def test_search_text_field_max_length(self):
        # get the search textbox
        search_field = self.driver.find_element_by_id("search")
        # check maxlength attribute is set to 128
        self.assertEqual("128", search_field.get_attribute("maxlength"))

    def test_search_button_enabled(self):
        # get Search button
        search_button = self.driver.find_element_by_class_name("button")
        # check Search button is enabled
        self.assertTrue(search_button.is_enabled())

    def test_my_account_link_is_displayed(self):
        # get the Account link
        account_link = self.driver.find_element_by_link_text("ACCOUNT")
        # check My Account link is displayed/visible in
        # the Home page footer
        self.assertTrue(account_link.is_displayed())

    def test_account_links(self):
        # get the all the links with Account text in it
        account_links = self.driver.find_elements_by_partial_link_text("ACCOUNT")
        # check Account and My Account link is
        # displayed/visible in the Home page footer
        self.assertTrue(3, len(account_links))

    def test_count_of_promo_banners_images(self):
        # get promo banner list
        banner_list = self.driver.find_element_by_class_name("promos")
        # get images from the banner_list
        banners = banner_list.find_elements_by_tag_name("img")
        # check there are 3 banners displayed on the page
        self.assertEqual(3, len(banners))

    def test_vip_promo(self):
        # get vip promo image
        vip_promo = self.driver.find_element_by_xpath("//img[@alt='Shop Private Sales - Members Only']")
        # check vip promo logo is displayed on home page
        self.assertTrue(vip_promo.is_displayed())
        # click on vip promo images to open the page
        vip_promo.click()
        # check page title
        self.assertEqual("VIP", self.driver.title)

    def test_shopping_cart_status(self):
        # check content of My Shopping Cart block
        # on Home page
        # get the Shopping cart icon and click to
        # open the Shopping Cart section
        shopping_cart_icon = self.driver.find_element_by_css_selector("div.header-minicart span.icon")
        shopping_cart_icon.click()
        # get the shopping cart status
        shopping_cart_status = self.driver.find_element_by_css_selector("p.empty").text
        self.assertEqual("You have no items in your shopping cart.", shopping_cart_status)
        # close the shopping cart section
        close_button = self.driver.find_element_by_css_selector("div.minicart-wrapper a.close")
        close_button.click()

    def test_language_options(self):
        # list of expected values in Language dropdown
        exp_options = ["ENGLISH", "FRENCH", "GERMAN"]
        # empty list for capturing actual options displayed
        # in the dropdown
        act_options = []
        # get the Your language dropdown as instance of Select class
        select_language = Select(self.driver.find_element_by_id("select-language"))
        # check number of options in dropdown
        self.assertEqual(3, len(select_language.options))
        # get options in a list
        for option in select_language.options:
            act_options.append(option.text)
        # check expected options list with actual options list
        self.assertListEqual(exp_options, act_options)
        # check default selected option is English
        self.assertEqual("ENGLISH", select_language.first_selected_option.text)
        # select an option using select_by_visible text
        select_language.select_by_visible_text("German")
        # check store is now German
        self.assertTrue("store=german" in self.driver.current_url)
        # changing language will refresh the page,
        # we need to get find language dropdown once again
        select_language = Select(self.driver.find_element_by_id("select-language"))
        select_language.select_by_index(0)

    @classmethod
    def tearDownClass(cls):
        # close the browser window
        cls.driver.quit()