__author__ = 'anna'
import pytest
from selenium import webdriver
from base.webdriver_factory import WebDriverFactory
from pages.home.login_page import LoginPage

#conftest is a configuration file for all the pytest files.
#if I have similar setup for all the tests in all files I can put this setup in conftest file

#method with decorator pytest.yield_fixture deprecated - use pytest.fixture instead: it has yield functionality also
#the code before yield is running before every test_method/class/etc (depends on defined scope)
#the code after yield is running after every test_method/class/etc (depends on defined scope)
#scope: by default scope = function
#scope = module (means .py pytest file)
#scope = class

@pytest.fixture()
def method_set_up(): #scope = function(method)
    print('Method setup')
    yield
    print('Method teardown')
# @pytest.fixture(scope='module')
# def module_set_up(browser, os_type):
#     print('Module setup')
#     if browser == 'Firefox':
#         print('Running test on FF')
#     else:
#         print('Running test on Chrome')
#
#     if os_type == 'Linux':
#         print('Running test on Linux')
#     else:
#         print('Running test on OS X')
#
#     # if server_time == "EST":
#     #     print('EST')
#     # else:
#     #     print("PDT")
#     yield
#     print('Module teardown')

#for letskodit
@pytest.fixture(scope='class')
def module_set_up_level_to_test_a_class(request, browser): # this is One time setup
    print('Module setup')
    webdriver_factory = WebDriverFactory(browser)
    driver = webdriver_factory.get_webdriver_instance_letskodit()
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    result = login_page.verify_redirected_to_login_page()
    #TODO add logging to this if-else: now when hitting else - printing to console
    if result:
        login_page.login("job@kirsanova.name", "Testpw")
    else:
        print('Result:{}: Not redirected to login page'.format(result))
    # base_url = "https://letskodeit.teachable.com"
    # if browser == 'Firefox':
    #     driver = webdriver.Firefox()
    #     driver.maximize_window()
    #     driver.implicitly_wait(3)
    #     driver.get(base_url)
    #     print('Running test on FF')
    # else:
    #     driver = webdriver.Chrome()
    #     driver.maximize_window()
    #     driver.implicitly_wait(3)
    #     driver.get(base_url)
    #     print('Running test on Chrome')

    # to pass value to the TestClassDemo2 if class requests it!! while initializing instance
    if request.cls:  #.cls - means class context (level)
        request.cls.driver = driver
    yield driver
    driver.quit()
    print('Module teardown')

#for orangehrm
@pytest.fixture(scope="class")
def module_set_up_level_to_test_a_class_orangehrm(request, browser): # this is One time setup
    print('Module setup')
    webdriver_factory = WebDriverFactory(browser)
    driver = webdriver_factory.get_webdriver_instance_hrm()
    login_page = LoginPage(driver)
    login_page.login_hrm("admin", "Bitnami.12345")
    # base_url = "http://localhost"
    # if browser == 'Firefox':
    #     driver = webdriver.Firefox()
    #     driver.maximize_window()
    #     driver.implicitly_wait(3)
    #     driver.get(base_url)
    #     print('Running test on FF')
    # else:
    #     driver = webdriver.Chrome()
    #     driver.maximize_window()
    #     driver.implicitly_wait(3)
    #     driver.get(base_url)
    #     print('Running test on Chrome')
    # to pass value to the TestClassDemo2 if class requests it!! while initializing instance
    if request.cls:  #.cls - means class context (level)
        request.cls.driver = driver
    yield driver
    driver.quit()
    print('Module teardown')

#from old conftest:
#adding options for CLI when running the funtion
def pytest_addoption(parser):
    parser.addoption("--browser")
    # parser.addoption("--osType", help="Type of operating system") #help - this is for the CLI user so he can understand what this option is about
    # parser.addoption("--serverTime", help="Type the server time")

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")

# @pytest.fixture(scope='session')
# def os_type(request):
#     return request.config.getoption("--osType")

# @pytest.fixture(scope='session')
# def server_time(request):
#     return request.config.getoption("--serverTime")
