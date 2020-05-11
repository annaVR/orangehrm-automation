"""
Base Page class
It implements methods which are common to all the pages of web application
This class needs to be inherited by all the page classes
This should not be used by creating object instances

Ex:
    Class LoginPage(BasePage):
"""

from base.selenium_driver import SeleniumDriver
from traceback import print_stack
from utilities.util import Util

class BasePage(SeleniumDriver):

    def __init__(self, driver):
        """
        Inits Base Page class
        :param driver:
        """

        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def verify_page_title(self, expected_title):
        """
        Vefify a page's Title
        :param expected_title: Expected title
        :return:
        """
        try:
            actual_title = self.get_title()
            return self.util.verify_text_contains(actual_title, expected_title)
        except:
            self.log.error("## Exception Occured: Failed to get page title")
            print_stack()
            return False