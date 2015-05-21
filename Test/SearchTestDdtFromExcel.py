
__author__ = 'yanaor'

import xlrd, unittest
from selenium import webdriver
from ddt import ddt, data, unpack


def get_data(file_name):
    # create an empty list to store rows
    rows = []
    # open the specified Excel spreadsheet as workbook
    book = xlrd.open_workbook(file_name)
    # get the first sheet
    sheet = book.sheet_by_index(0)
    # iterate through the sheet and get data from rows in list
    for row_idx in range(1, sheet.nrows):rows.append(list(sheet.row_values(row_idx, 0, sheet.ncols)))
    return rows

@ddt
class SearchDDT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # create a new Firefox session
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("http://demo.magentocommerce.com/")

    # specify test data using @data decorator
    @data(*get_data("TestData.xlsx"))
    @unpack
    def test_search(self, search_value, expected_count):
        # get the search textbox
        self.search_field = self.driver.find_element_by_name("q")
        self.search_field.clear()
        # enter search keyword and submit.
        # use search_value argument to pass data
        self.search_field.send_keys(search_value)
        self.search_field.submit()
        # get all the anchor elements which have
        # product names displayed
        # currently on result page using
        # find_elements_by_xpath method
        products = self.driver.find_elements_by_xpath("//h2[@class='product-name']/a")
        expected_count = int(expected_count)
        if expected_count > 0:
            # check count of products shown in results
            self.assertEqual(expected_count, len(products))
        else:
            msg = self.driver.find_element_by_class_name("note-msg")
            self.assertEqual("Your search returns no results.", msg.text)
    @classmethod
    def tearDownClass(self):
        # close the browser window
        self.driver.quit()
  #  if __name__ == '__main__':
    #    unittest.main()__author__ = 'yanaor'
