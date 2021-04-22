import time
from base.base_page import BasePage
import utilities.custom_logger as cl
import logging


class RegisterCoursesPage(BasePage):

    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #Locators
    _search_box = "//div[@class='input-group']//input[@id='search-courses']" #xpath
    _mac_linux_course = "//div[@class='col-lg-12']//div[@title='Mac Linux Command Line Basics']" #xpath
    _all_cources = "//div[@class='row course-list list']//div[@class='course-listing-title']"
    _search_course_button = 'search-course-button' #id
    _course = "//div[contains(@class,'course-listing-title') and contains(text(),'{0}')]"
    _course_curriculum_header = "//div[@class='container']//h2[contains(text(), 'Course Curriculum')]"
    _enroll_button_top = "//button[@id='enroll-button-top']"
    _payment_information_header = "//section[@class='spc__section']//div[text()='Payment Information']"
    _cc_number_iframe_name = "__privateStripeFrame12"
    _cc_number = "//span//input[@name='cardnumber']"
    _cc_expiration_date_iframe_name = "__privateStripeFrame13"
    _cc_expiration_date = "//span//input[@name='exp-date']"
    _cc_cvc_iframe_name = "__privateStripeFrame14"
    _cc_cvc = "//span//input[@name='cvc']"
    _country_dropdown = "//div[@class='form-group']//select[@name='country_code']" # it may return 2 nodes
    _postal_code_iframe_name = "__privateStripeFrame15"
    _postal_code = "zipCode" #id
    _buy_now_button = "//div[@class='m-b-4-xs _3pM7B']//button[@data-test='confirm-enroll']"
    _agreed_to_terms_checkbox = "//section[@class='spc__section spc__section--terms']" \
                                "//input[@id='agreed_to_terms_checkbox']"
    _use_another_card = "//div[@class='p-3-xs']//button[text()='Use another card']"

    #elements actions
    def enter_course_name(self, course_name):
        self.send_Keys(course_name, self._search_box, locator_type="xpath")

    def click_search_for_course_button(self):
        self.element_click(self._search_course_button, locator_type='id')

    def select_course_to_enroll(self, full_course_name):
        self.element_click(locator=self._course.format(full_course_name), locator_type="xpath")

    def select_mac_linux_course(self):
        self.element_click(self._mac_linux_course, locator_type="xpath")

    def click_enroll_button_top(self):
        self.element_click(self._enroll_button_top, locator_type="xpath")

    def click_use_another_card(self):
        self.element_click(self._use_another_card, locator_type="xpath")
        time.sleep(3)

    def enter_cc_number(self, cc_number):
        #this is to handle dinamic iframe. In real work situation the dinamic iframe is bad practice
        # Frame takes 6 seconds to show, even more
        time.sleep(6)
        #self.switch_to_frame(name=self._cc_number_iframe_name)
        self.switch_frame_by_index(self._cc_number, locator_type="xpath")
        self.send_Keys(cc_number, self._cc_number, locator_type="xpath")
        self.switch_to_default_content()

    def enter_exp_date(self, exp_date):
        #self.switch_to_frame(name=self._cc_expiration_date_iframe_name)
        self.switch_frame_by_index(self._cc_expiration_date, locator_type="xpath")
        self.send_Keys(exp_date, self._cc_expiration_date, locator_type="xpath")
        self.switch_to_default_content()

    def enter_cvc(self, cvc):
        #self.switch_to_frame(name=self._cc_cvc_iframe_name)
        self.switch_frame_by_index(self._cc_cvc, locator_type="xpath")
        self.send_Keys(cvc, self._cc_cvc, locator_type="xpath")
        self.switch_to_default_content()

    def enter_postal_code(self,postal_code):
        #self.switch_to_frame(name=self._postal_code_iframe_name)
        self.switch_frame_by_index(self._postal_code, locator_type="id")
        self.send_Keys(postal_code, self._postal_code, locator_type="id")
        self.switch_to_default_content()

    def click_buy_now_button(self):
        self.element_click(self._buy_now_button, locator_type="xpath")

    # TODO start here and in register_courses_tests
    # try the 2 following methods and see if they work correctly
    def select_agreed_checkbox(self):
        selected = self.select_checkbox(self._agreed_to_terms_checkbox, locator_type='xpath')

    def unselect_agreed_checkbox(self):
        unselected = self.unselect_checkbox(self._agreed_to_terms_checkbox, locator_type="xpath")

    #main functions
    def search_for_course(self, course_name=''): #parameters are optional - to test search for empty course
        self.enter_course_name(course_name)
        self.click_search_for_course_button()

    def verify_redirected_to_course_details_page(self):
        self.web_scroll(direction='down')
        result = self.is_element_present(self._course_curriculum_header, locator_type="xpath")
        self.web_scroll(direction="up")
        return result

    def enroll_in_course_from_course_details_page(self):
        self.click_enroll_button_top()

    def verify_redirected_to_checkout_page(self):
        result = self.is_element_present(self._payment_information_header, "xpath")
        return result

    def enter_another_card_details_postal_code(self, cc_number="", exp_date="", cvc="", postal_code=""):
        self.web_scroll(direction="down")
        self.click_use_another_card()
        self.enter_cc_number(cc_number)
        self.enter_exp_date(exp_date)
        self.enter_cvc(cvc)
        self.enter_postal_code(postal_code)

    def verify_buy_now_button_disabled(self):
        result = not self.isEnabled(self._buy_now_button, locator_type="xpath", info="Buy Now Button")
        return result

    def verify_buy_now_button_enabled(self):
        result = self.isEnabled(self._buy_now_button, locator_type="xpath", info="Buy Now Button")
        return result

    def clear_cc_fields(self):
        self.clear_field(self._cc_number, locator_type="xpath")
        self.clear_field(self._cc_expiration_date, locator_type="xpath")
        self.clear_field(self._cc_cvc, locator_type="xpath")
        self.clear_field(self._postal_code, locator_type="xpath")

