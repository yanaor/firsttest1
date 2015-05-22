
__author__ = 'yanaor'

import xlrd, unittest
from selenium import webdriver
from ddt import ddt, data, unpack


def get_data(file_name):
    rows = []
    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_index(0)
    for row_idx in range(1, sheet.nrows):rows.append(list(sheet.row_values(row_idx, 0, sheet.ncols)))
    return rows


@ddt
class Authorization(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://yanaorlova.vaimo.com/")

    @data(*get_data('ValidData.xlsx'))
    @unpack
    def test_valid_login(self, email, password, firstname, lastname):
        self.driver.find_element_by_link_text('LOG IN').click()
        emailadressfield = self.driver.find_element_by_id("email")
        emailadressfield.clear()
        emailadressfield.send_keys(email)
        passwordfield = self.driver.find_element_by_id("pass")
        passwordfield.clear()
        passwordfield.send_keys(password)
        passwordfield.submit()
        greeting = self.driver.find_element_by_class_name("hello").text
        self.assertEqual(greeting, "Hello, %s %s!" % (firstname, lastname))
        logout = self.driver.find_element_by_link_text("LOG OUT")
        self.assertTrue(logout.is_displayed())

    @data(*get_data('InvalidData.xlsx'))
    @unpack
    def test_invalid_login(self, email, password):
        self.driver.find_element_by_link_text('LOG IN').click()
        emailadressfield = self.driver.find_element_by_id("email")
        emailadressfield.clear()
        emailadressfield.send_keys(email)
        passwordfield = self.driver.find_element_by_id("pass")
        passwordfield.clear()
        if len(password)>=6:
            passwordfield.send_keys(password)
            passwordfield.submit()
            errormessage = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li/ul/li/span").text
            self.assertEqual(errormessage, "Invalid login or password.")
        else:
            passwordfield.send_keys(password)
            passwordfield.submit()
            validation_advice = self.driver.find_element_by_id("advice-validate-password-pass").text
            self.assertEqual(validation_advice, "Please enter 6 or more characters. Leading or trailing spaces will be ignored.")


    @classmethod
    def tearDown(self):
        self.driver.quit()
