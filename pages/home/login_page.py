import time
from base.base_page import BasePage
from pages.home.navigation_page import NavigationPage
import utilities.custom_logger as cl
import logging


class LoginPage(BasePage):

    #getting the log in this class, so the name of the class will show up in logs
    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)  # calling the __init__ method of the super class (Selenium Driver) and providing the driver to it
        self.driver = driver
        self.navigation = NavigationPage(self.driver)

    # Locators letscodeit
    _login_link = "Login" #locator: link
    _email_field = 'user_email'#locator: id
    _password_field = "user_password" #locator: id
    _login_button = "commit" #locator: name

    # Locators orangehrm
    _username_field_hrm = "//div[@id='divUsername']/input[@id='txtUsername']" #locator: xpath
    _password_field_hrm = "txtPassword" #locator: id
    _login_button_hrm = "btnLogin" #locator: id

    # Elements actions
    # letscodit
    def click_login_link(self):
        self.element_click(self._login_link, locator_type='link')

    def enter_email(self, email):
        self.send_Keys(email, self._email_field) #not providing locator_type because using 'id' default one

    def clear_email(self):
        self.clear_field(self._email_field)

    def enter_password(self, password):
        self.send_Keys(password, self._password_field)

    def click_login_button(self):
        self.element_click(self._login_button, locator_type="name")

    # hrm
    def enter_username_hrm(self, username):
        self.send_Keys(username, self._username_field_hrm, locator_type="xpath")

    def clear_username_hrm(self):
        self.clear_field(self._username_field_hrm, locator_type="xpath")

    def clear_password_hrm(self):
        self.clear_field(self._password_field_hrm, locator_type="id")

    def enter_password_hrm(self, password):
        self.send_Keys(password, self._password_field_hrm)

    def click_login_button_hrm(self):
        self.element_click(self._login_button_hrm)

    # Main functions
    # letscodit
    def go_to_login_page(self):
        self.click_login_link()

    def login(self, email='', password=''): #parameters are optional e.g. for testing empty credentials
        self.clear_email()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def verify_redirected_to_login_page(self):
        result = self.is_element_present(self._login_button, locator_type="name")
        return result

    def verify_login_successful(self):
        result = self.is_element_present("//div[@id='navbar']//li[@class='dropdown']", locator_type="xpath")
        return result # returns boolean

    def verify_login_failed(self):
        result = self.is_element_present("//div[contains(text(), 'Invalid email or password')]", locator_type="xpath")
        return result

    def verify_login_title(self):
        return self.verify_page_title(expected_title="Let's Kode")

    def logout(self):
        self.navigation.navigate_profile_icon()
        element = self.wait_for_element(locator='//div//a[@href="/sign_out"]', locator_type='xpath', pollFrequency=1)
        self.element_click(element=element)


    # hrm
    def login_hrm(self, username='', password=''):
        self.clear_username_hrm()
        self.clear_password_hrm()
        self.enter_username_hrm(username)
        time.sleep(2)
        self.enter_password_hrm(password)
        time.sleep(2)
        self.click_login_button_hrm()

    def verify_login_successfull_hrm(self):
        result = self.is_element_present("//div[@id='branding']//a[text()='Welcome User']", locator_type='xpath')
        return result # returns boolean

    def verify_login_failed_hrm(self):
        result = self.is_element_present("//div//span[text()='Invalid credentials']", locator_type="xpath")
        return result

    def verify_empty_username_login_failed_hrm(self):
        result = self.is_element_present("//div[@id='divLoginButton']//span[text()='Username cannot be empty']", locator_type="xpath")
        return result

    def verify_login_title_hrm(self):
        return self.verify_page_title(expected_title="OrangeHRM")

    def logout_hrm(self):
        self.navigation.logout()
# 4. observe recent changed and remove that is not needed