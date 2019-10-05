from selenium import webdriver
from pages.home.login_page import LoginPage
import unittest
import pytest
import time


class LoginTests(unittest.TestCase):
    base_url = "https://letskodeit.teachable.com"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(base_url)
    login_page = LoginPage(driver)

    @pytest.mark.run(order=1)
    def test_go_to_login_page(self):
        self.login_page.go_to_login_page()
        result = self.login_page.verify_redirected_to_login_page()
        assert result is True

    @pytest.mark.run(order=3)
    def test_valid_login(self):

        self.login_page.login("test@email.com", "abcabc")
        result = self.login_page.verify_login_successfull()
        assert result is True
        time.sleep(5)
        self.driver.quit()

    @pytest.mark.run(order=2)
    def test_invalid_login(self):
        self.login_page.login("test@email.com", "abcabcbbb")
        result = self.login_page.verify_login_failed()
        assert result is True

