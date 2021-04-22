from selenium import webdriver
from pages.home.login_page import LoginPage
from utilities.tc_status import TCaseStatus
import unittest
import pytest
import time

#the only "module_set_up_level_to_test_a_class" fixture is doing something useful, the other is just does print statements
@pytest.mark.usefixtures("module_set_up_level_to_test_a_class_orangehrm", "method_set_up")
class LoginHrmTests(unittest.TestCase):

    # base_url = "http://localhost"
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.implicitly_wait(3)
    # driver.get(base_url)

    # create class_level fixture to prepare to run all tests: here to make an instance of a class we are testing and
    # make it available to every method
    @pytest.fixture(autouse=True)
    def class_setup(self, module_set_up_level_to_test_a_class_orangehrm):  # need to provide fixture to the class here because we need to get the "value" returned by request.cls.value
        self.login_page = LoginPage(self.driver)
        self.test_status = TCaseStatus(self.driver)

    @pytest.mark.run(order=4)
    def test_valid_login(self):
        #after 186 video we login via conftest setup class method as a precondition to write the rest of TCs
        #--> will deal with that later for login tests
        self.login_page.login_hrm("admin", "Bitnami.12345")
        result1 = self.login_page.verify_login_title_hrm()
        self.test_status.mark(result1, "Title Verification")
        time.sleep(2)
        result2 = self.login_page.verify_login_successfull_hrm()
        #call mark_final() at the last test in the Test Case with multiple assertions
        self.test_status.mark_final("Test Case Name: test_valid_login", result2, "Login Successful Verification")
        #self.driver.quit() - moved to conftest.py >> pytest fixture

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        self.login_page.logout_hrm()
        self.login_page.login_hrm("longinvalid", "abcabcbbb")
        result = self.login_page.verify_login_failed_hrm()
        assert result is True

    @pytest.mark.run(order=2)
    def test_empty_credentials_login(self):
        self.login_page.login_hrm()
        result = self.login_page.verify_empty_username_login_failed_hrm()
        assert result is True

    @pytest.mark.run(order=3)
    def test_empty_username_valid_password_login(self):
        self.login_page.login_hrm(password="Bitnami.12345")
        result = self.login_page.verify_empty_username_login_failed_hrm()
        assert result is True