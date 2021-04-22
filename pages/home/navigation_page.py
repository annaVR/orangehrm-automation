import time
from base.base_page import BasePage
import utilities.custom_logger as cl
import logging
from selenium.webdriver import ActionChains

class NavigationPage(BasePage):
    #page: https://letskodeit.teachable.com/courses

    #getting the log in this class, so the name of the class will show up in logs
    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)  # calling the __init__ method of the super class (Selenium Driver) and providing the driver to it
        self.driver = driver

    # Locators letscodeit
    _my_courses ='//a[@href="/courses/enrolled"]'
    _all_courses = '//a[@href="/courses"]'
    _practice = '//a[@href="/pages/practice"]'
    _profile_icon = '//img[@class="gravatar"]'
    _letskodeit_icon = '//div/a[@class="navbar-brand header-logo"]'

    # Locators orangehrm
    #TODO
    #_welcome_user = "welcome" #id
    _welcome_user = "//div[@id='branding']//a[text()='Welcome User']"
    _logout = "//div[@id='welcome-menu']//a[text()='Logout']"
    #_logout = "//div//a[text()='Logout']"

    # Elements actions
    # letscodit

    def navigate_to_all_courses(self):
        self.element_click(self._all_courses, locator_type='xpath')

    def navigate_to_my_courses(self):
        self.element_click(self._my_courses, locator_type='xpath')

    def navigate_to_practice(self):
        self.element_click(self._practice, locator_type='xpath')

    def navigate_profile_icon(self):
        element = self.wait_for_element(self._profile_icon, locator_type='xpath', pollFrequency=1)
        self.element_click(element=element)

    def navigate_to_letskodeit_icon(self):
        self.element_click(self._letskodeit_icon, locator_type='xpath')

    # hrm
    def select_welcome_user(self):
        welcome_user_element = self.driver.find_element_by_xpath(self._welcome_user)
        #used ActionChains because regular click() was not working on this element
        ActionChains(self.driver).move_to_element(welcome_user_element).click(welcome_user_element).perform()

    def select_logout(self):
        logout_element = self.wait_for_element(locator=self._logout,
                                               locator_type='xpath', pollFrequency=1)
        self.element_click(element=logout_element)

    # Main functions
    # letscodit
    # hrm

    def logout(self):
        self.select_welcome_user()
        self.select_logout()
