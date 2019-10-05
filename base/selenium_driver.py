__author__ = 'anna'

from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import unilities.custom_logger as cl
import logging
import sys

class SeleniumDriver():

    #getting logger from custom_logger class
    log = cl.CustomLogger(logging.DEBUG)  #setting the logging level via logging.DEBUG

    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        else:
            self.log.warning("Locator type " + locator_type + " not correct/supported")
        return False

    def get_element(self, locator, locator_type="id"):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info("Element Found with locator '{}' and locator_type '{}'".format(locator, locator_type))
        except:
            self.log.error("Element not found with locator '{}' and locator_type '{}'".format(locator, locator_type))
        return element

    def element_click(self, locator, locator_type='id'):

        try:
            element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("Click on element with locator '{}' and locator_type '{}'".format(locator, locator_type))
        except:
            self.log.error("Cannot click on the element with locator '{}' and locator_type '{}'".format(locator, locator_type))
            print_stack()
            print('Unexpected error', sys.exc_info())

    def send_Keys(self, data, locator, locator_type='id'):

        try:
            element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info("Sent data to element with locator '{}' and locator_type '{}'".format(locator, locator_type))
        except:
            self.log.error("Cannot send data to the element with locator '{}' and locator_type '{}'".format(locator, locator_type))
            print_stack()

    def clear_field(self, locator, locator_type='id'):
        try:
            element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info("Cleared data of element with locator '{}' and locator_type '{}'".format(locator, locator_type))
        except:
            self.log.error("Cannot clear data of element with locator '{}' and locator_type '{}'".format(locator, locator_type))
            print_stack()

    #using our function get_by_type in this function
    def is_element_present(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        if element is None: # if element returning none that means it is not exist - see get_element()
            return False
        else:
            return True


    #using class By.type as an argument
    def is_element_present_list_method(self, by_type, locator):
        elements_list = self.driver.find_elements(by_type, locator)
        if len(elements_list) > 0:
            return True
        else:
            return False

    def wait_for_element(self, locator, locator_type="id",
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.error("Element not appeared on the web page")
            print_stack()
        return element