"""
WebDriverFactory class
It creates a webdriver instance based on browser configuration
Example:
    webdriver_factory = WebDriverFactory(browser)
    driver = webdriver_factory.get_webdriver_instance()
"""
import traceback
from selenium import webdriver


class WebDriverFactory():

    def __init__(self, browser):

        """
        Inits WebDriverFactory class

        :param browser:

        Returns:
            None
        """
        self.browser = browser

    def get_webdriver_instance_letskodit(self):
        """

        :return: webdriver instance based on parameters
        """
        base_url = "https://letskodeit.teachable.com"
        if self.browser == "Firefox":
            driver = webdriver.Firefox()
        else:
            #captcha workaround 2 next lines of code
            #chrome://version/
            #on the first run - fillout captcha manually and then quit the browser,on next runs,captcha should disappear
            opt = webdriver.ChromeOptions()
            opt.add_argument("user-data-dir=/Users/annaromanovskaia/Library/Application Support/Google/Chrome/Default")
            driver = webdriver.Chrome(options=opt)

        driver.implicitly_wait(3)
        driver.maximize_window()
        driver.get(base_url)
        return driver

    def get_webdriver_instance_hrm(self):
        """

        :return: webdriver instance based on parameters
        """
        base_url = "http://localhost"
        if self.browser == "Firefox":
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Chrome()

        driver.implicitly_wait(3)
        driver.maximize_window()
        driver.get(base_url)
        return driver