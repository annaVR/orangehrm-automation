__author__ = 'anna'

from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
import logging
import sys
import datetime
import os

#TODO rewrite except blocks to return exception errors

class SeleniumDriver():

    #getting logger from custom_logger class
    #log = cl.CustomLogger(logging.DEBUG)  #setting the logging level via logging.DEBUG - disabled for now as log coming from login_page.py
    #enable if needed

    def __init__(self, driver):
        self.driver = driver

    def screenshot(self, result_message):
        """
        Takes screenshot of the current open web page and saves it in screenshots folder
        :param result_message:
        :return:
        """
        file_name = "{}.{}.png".format(result_message, datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S"))
        screenshot_directory = "../screenshots/"
        relative_filename = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, relative_filename)
        destination_directory = os.path.join(current_directory, screenshot_directory)
        self.log.info("Destination directory: {} Dest file: {}".format(destination_directory, destination_file))

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            try:
                self.driver.save_screenshot(destination_file)
                self.log.info("Screenshot saved to: {}.".format(destination_file))
            except:
                self.log.error("Path found: {}, but unable to save screenshot {}.".format
                               (destination_directory, destination_file))
                print_stack()
        except:
            self.log.error("## Exception Occured While Taking Screenshot")
            print_stack()

    def get_title(self):
        return self.driver.title

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

    def get_elements_list(self, locator, locator_type="id"):
        """
        New
        Returns elements list
        :param locator:
        :param locator_type:
        :return: Returns elements list
        """
        elements_list = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            elements_list = self.driver.find_elements(by_type, locator)
            self.log.info("Elements List Found with locator '{}' and locator_type '{}'".format
                          (locator, locator_type))
        except:
            self.log.error("Elements List Not Found with locator '{}' and locator_type '{}'".format
                           (locator, locator_type))
        return elements_list

    def element_click(self, locator="", locator_type="id", element=None):
        """
        Either provide element or locator/locator_type
        :param locator:
        :param locator_type:
        :param element:
        :return: None
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("Clicked on element '{}' with locator '{}' and locator_type '{}'".format
                          (element, locator, locator_type))
        except:
            self.log.error("Cannot click on element '{}' with locator '{}' and locator_type '{}'".format
                           (element, locator, locator_type))
            print_stack()
            #print('Unexpected error', sys.exc_info())

    def send_Keys(self, data, locator, locator_type='id', element=None):
        """
        Arguments: provide either element or a locator/locator_type combination
        :param data:
        :param locator:
        :param locator_type:
        :param element:
        :return: None
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info("Sent data to element '{}' with locator '{}' and locator_type '{}'".format
                          (element, locator, locator_type))
        except:
            self.log.error("Cannot send data to the element '{}' with locator '{}' and locator_type '{}'".format
                           (element, locator, locator_type))
            print_stack()

    def clear_field(self, locator, locator_type='id'):
        try:
            element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info("Cleared data of element with locator '{}' and locator_type '{}'".format(locator, locator_type))
        except:
            self.log.error("Cannot clear data of element with locator '{}' and locator_type '{}'".format(locator, locator_type))
            print_stack()

    def get_text(self, locator="", locator_type="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type conbination
        """
        try:
            if locator:  # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.get_element(locator, locator_type)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, text length is: {}".format(str(len(text))))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text of element {}".format(info))
                self.log.info("The text is {}".format(text))
                text = text.strip()
        except:
            self.log.error("Failed to get text of element {}".format(info))
            print_stack()
            text = None
        return text

    #using our function get_by_type in this function
    def is_element_present(self, locator, locator_type="id", element=None):
        """
        Arguments: either provide element or locator/locator_type combination
        :param locator:
        :param locator_type:
        :return: True or False
        !!!!Check if logic is correct - compare with modified method if it is not working!!!!
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is None: # if element returning none that means it is not exist - see get_element()
                self.log.info("Element '{}' is not present with locator '{}' and locator_type '{}'".format
                              (element, locator, locator_type))
                return False
            else:
                self.log.info("Element '{}' present with locator '{}' and locator_type '{}'".format
                              (element, locator, locator_type))
                return True

        except:
            self.log.error("## Except Block: Element not found")
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of locator and locator_type
        """
        # TODO check logic, what to return in except block. Also keep in mind what to be returned to
        is_displayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed with locator:{} and locator_type:{}".format(locator, locator_type))
            else:
                self.log.info("Element is not displayed with locator:{} and locator_type:{}".format(locator, locator_type))
            return is_displayed
        except:
            self.log.error("## Except Block: Element not found")
            return False

    def is_selected_selected(self, locator="", locator_type="id", element=None):
        """
        mine METHOD - copied from is_displayed
        Check if element is selected (checkbox or radio button)
        Either provide element or a combination of locator and locator_type
        """
        #TODO check logic, what to return in except block. Also keep in mind what to be returned to
        #TODO select_checkbox and unselect_ckeckbox (see below)
        is_selected = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_selected = element.is_selected()
                self.log.info("Element (checkbox/radio) is selected"
                              " with locator:{} and locator_type:{}".format(locator, locator_type))
            else:
                self.log.info("Element (checkbox/radio) is not selected"
                              " with locator:{} and locator_type:{}".format(locator, locator_type))
            return is_selected
        except:
            self.log.error("## Except Block: Element not found")
            return False

    def select_checkbox(self, locator, locator_type):
        #mine
        #TODO check logic, what to return in except block. Also keep in mind what returned by
        #TODO _is_element_selected (see above)
        is_selected = self.is_element_selected(locator, locator_type)
        try:
            if is_selected is True:
                self.log.info("Checkbox/radio with locator:{} and locator_type:{} was already selected"
                              .format(locator, locator_type))
                pass
            elif is_selected is False:
                self.element_click(locator, locator_type)
                self.log.info("Clicked on element Checkbox/radio with locator:{} and locator_type:{}"
                              .format(locator, locator_type))
        except:
            self.log.error("## Exception Occurs: Cannot select checkbox with locator {}"
                           "and locator_type {}".format(locator, locator_type))

    def unselect_checkbox(self, locator, locator_type):
        #mine
        # TODO check logic, what to return in except block. Also keep in mind what returned by
        # TODO _is_element_selected (see above)
        is_selected = self.is_element_selected(locator, locator_type)
        try:
            if is_selected is True:
                self.element_click(locator, locator_type)
                self.log.info("Unselected Checkbox/radio with locator:{} and locator_type:{}"
                              .format(locator, locator_type))
            elif is_selected is False:
                self.log.info("Element Checkbox/radio with locator:{} and locator_type:{} was already unselected"
                              .format(locator, locator_type))
                pass
        except:
            self.log.error("## Exception Occurs: Cannot unselect checkbox with locator {}"
                           "and locator_type {}: None returned".format(locator, locator_type))

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

    def web_scroll(self, direction="up"):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

#did not checked the logic for the following methods:
    def switch_to_frame(self, id="", name="", index=None):
        """
        Switch to iframe using element locator inside iframe

        Parameters:
            1. Required:
                None
            2. Optional:
                1. id    - id of the iframe
                2. name  - name of the iframe
                3. index - index of the iframe
        Returns:
            None
        Exception:
            None
        """
        if id:
            self.driver.switch_to.frame(id)
        elif name:
            self.driver.switch_to.frame(name)
        else:
            self.driver.switch_to.frame(index)


    def switch_to_default_content(self):
        """
        Switch to default content
        Parameters:
            None
        Returns:
            None
        Exception:
            None
        """
        self.driver.switch_to.default_content()

    def get_element_attribute_value(self, attribute, element=None, locator="", locator_type="id"):
        """
        Get value of the attribute of element

        Parameters:
            1. Required:
                1. attribute - attribute whose value to find

            2. Optional:
                1. element   - Element whose attribute need to find
                2. locator   - Locator of the element
                3. locatorType - Locator Type to find the element

        Returns:
            Value of the attribute
        Exception:
            None
        """
        if locator:
            element = self.get_element(locator=locator, locator_type=locator_type)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator, locator_type="id", info=""):
        """
        Check if element is enabled

        Parameters:
            1. Required:
                1. locator - Locator of the element to check
            2. Optional:
                1. locatorType - Type of the locator(id(default), xpath, css, className, linkText)
                2. info - Information about the element, label/name of the element
        Returns:
            boolean
        Exception:
            None
        """
        element = self.get_element(locator, locator_type=locator_type)
        enabled = False
        try:
            attribute_value = self.get_element_attribute_value(element=element, attribute="disabled")
            if attribute_value is not None:
                enabled = element.is_enabled()
            else: #wrinting this else because ._is_enabled() Selenium built-in method works only if
                # there is an attribute 'disabled' specified in the element
                # in our case it does not exist, instead the word disabled specified in class name
                value = self.get_element_attribute_value(element=element, attribute="class")
                self.log.info("Attribute value From Application Web UI {}".format(value))
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("Element {} is enabled".format(info))
            else:
                self.log.info("Element {} is not enabled".format(info))
        except:
            self.log.error("## Except Block: Element {} state could not be found".format(info))
        return enabled
