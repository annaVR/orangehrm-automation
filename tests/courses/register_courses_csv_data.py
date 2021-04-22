from pages.courses.register_courses_page import RegisterCoursesPage
from pages.home.navigation_page import NavigationPage
from utilities.tc_status import TCaseStatus
import unittest
import pytest
import time
from ddt import ddt, data, unpack
from utilities.read_data import get_csv_data
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("module_set_up_level_to_test_a_class", "method_set_up")
@ddt
class RegisterCoursesCsvDataTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def class_setup(self, module_set_up_level_to_test_a_class):
        self.register_courses = RegisterCoursesPage(self.driver)
        self.test_status = TCaseStatus(self.driver)
        self.navigation = NavigationPage(self.driver)

    def setUp(self):
        #this is setup: since all tests for register courses should start on that page
        self.navigation.navigate_to_letskodeit_icon()

    @pytest.mark.run(order=1)
    @data(*get_csv_data("/Users/annaromanovskaia/PycharmProjects/orangehrm-automation/test_data_courses.csv"))
    @unpack
    def test_redirected_to_course_detail_page_and_invalid_enrollment(self, course_name, cc_number,
                                                                     cc_exp_date, cc_cvc, cc_postal_code):
        self.register_courses.search_for_course(course_name)
        # start from there
        self.register_courses.select_course_to_enroll(course_name)
        #self.register_courses.select_mac_linux_course()
        #result = self.register_courses.verify_redirected_to_course_details_page()
        #self.test_status.mark(result, "Redirected to course details page Verification")
        time.sleep(2)


    #def test_verify_enroll_button_final_disabled_with_invalid_card(self):
        self.register_courses.enroll_in_course_from_course_details_page()
        result2 = self.register_courses.verify_redirected_to_checkout_page()
        self.test_status.mark(result2, "Redirected to Checkout Page Verification")
        self.register_courses.enter_another_card_details_postal_code(cc_number=cc_number, exp_date=cc_exp_date,
                                                             cvc=cc_cvc, postal_code=cc_postal_code)
        result3 = self.register_courses.verify_buy_now_button_disabled()
        print("Result3: {}".format(result3))
        time.sleep(1)

        self.test_status.mark_final("Test Case Name: test_verify_enroll_button_final_disabled_with_invalid_card",
                              result3, "Enroll Button Final Disabled Verification")
        time.sleep(2)
