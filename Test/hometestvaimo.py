
__author__ = 'yanaor'

from selenium import webdriver
from ddt import ddt, data, unpack
import xlrd, unittest


def get_data(file_name):
    rows = []
    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_index(0)
    for row_idx in range(1, sheet.nrows):rows.append(list(sheet.row_values(row_idx, 0, sheet.ncols)))
    return rows

@ddt
class authorization(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://yanaorlova.vaimo.com/")

    @data(*get_data("Data.xlsx"))
    @unpack
    def validlogin(self, email, password, firstname, lastname):
        self.find_element_by_link_text("LOG IN").click()
        self.emailadressfield = self.driver.find_element_by_id("email")
        self.emailadressfield.clear()
        self.emailadressfield.send_keys(email)
        self.passwordfield = self.driver.find_element_by_id("pass")
        self.passwordfield.clear()
        self.passwordfield.send_keys(password)
        greeting = self.driver.find_element_by_class("hello").text
        self.assertEqual(greeting, "Hello,% %!" %(firstname, lastname))
        self.assertTrue(self.find_element_by_link_text("Log Out").is_displayed())

    @classmethod
    def tearDownClass(self):
        self.driver.quit()