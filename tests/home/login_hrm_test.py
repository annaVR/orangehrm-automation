from selenium import webdriver
from pages.home.login_page import LoginPage
import unittest
import pytest
import time


class LoginHrmTests(unittest.TestCase):

    base_url = "http://localhost"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(base_url)
    login_page = LoginPage(driver)

    @pytest.mark.run(order=2)
    def test_valid_login(self):

        self.login_page.login_hrm("admin", "Bitnami.12345")
        time.sleep(3)
        result = self.login_page.verify_login_successfull_hrm()
        assert result is True
        self.driver.quit()

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        self.login_page.login_hrm("longinvalid", "abcabcbbb")
        result = self.login_page.verify_login_failed_hrm()
        assert result is True
