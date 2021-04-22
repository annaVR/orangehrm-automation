from pages.courses.register_courses_page import RegisterCoursesPage
from utilities.tc_status import TCaseStatus
import unittest
import pytest
import time
#the NavigationPage test in logs fails    when running test second and following time,
# because user already logged
@pytest.mark.usefixtures("module_set_up_level_to_test_a_class", "method_set_up")
class RegisterCoursesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def class_setup(self, module_set_up_level_to_test_a_class):
        self.register_courses = RegisterCoursesPage(self.driver)
        self.test_status = TCaseStatus(self.driver)

    @pytest.mark.run(order=1)
    def test_redirected_to_course_detail_page(self):
        self.register_courses.search_for_course("Mac Linux Command Line Basics")
        self.register_courses.select_mac_linux_course()
        result = self.register_courses.verify_redirected_to_course_details_page()
        self.test_status.mark_final("Test Case Name: test_redirected_to_course_detail_page", result,
                                    "Redirected to course details page Verification")
        time.sleep(4)

    @pytest.mark.run(order=2)
    def test_verify_buy_now_button_disabled_with_invalid_card(self):
        self.register_courses.enroll_in_course_from_course_details_page()
        result = self.register_courses.verify_redirected_to_checkout_page()
        self.test_status.mark(result, "Redirected to Checkout Page Verification")
        self.register_courses.enter_another_card_details_postal_code(cc_number="5555", exp_date="03/22",
                                                             cvc="123", postal_code="93405")
        result2 = self.register_courses.verify_buy_now_button_disabled()
        print("Result2: {}".format(result))
        time.sleep(3)

        self.test_status.mark_final("Test Case Name: test_verify_buy_now_button_disabled_with_invalid_card",
                              result2, "Buy Now Disabled Verification")
        time.sleep(3)
