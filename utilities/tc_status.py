from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging
from traceback import print_stack

class TCaseStatus(SeleniumDriver):

    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        """
        initiates Checkpoint class
        :param driver:
        """
        super(TCaseStatus, self).__init__(driver)
        self.results_list = []

    def set_result(self, result, result_message):
       try:
           if result is not None: # True or False
               if result: # if True
                   self.results_list.append('PASS')
                   self.log.info("## Verification Successful: {}".format(result_message))
               else: # if False
                   self.results_list.append('FAIL')
                   self.log.error("## Verification Failed: {}".format(result_message))
                   self.screenshot(result_message)
           else: # if None for example - maybe need different value to append?
               self.results_list.append('FAIL')
               self.log.error("## Verification Failed: {} Expected results True or False, but Returned:{}".format(result_message, result))
               self.screenshot(result_message)
       except: # if Something else happend - maybe need different value to append?
           self.results_list.append('FAIL')
           self.log.error("## Exception Occured While Evaluating Test Result!: {}. Expected results True or False, but Returned:{}".format(result_message, result))
           self.screenshot(result_message)
           print_stack()

    def mark(self, result, result_message):
        """
        Marks the result of the verification point in a test case
        :param result:
        :param result_message:
        :return:
        """
        self.set_result(result, result_message)

    def mark_final(self, test_name, result, result_message):
        """
        Marks the final result in the test case. This will the Test case final status.
        Called once per Test Case
        :param test_name:
        :param result:
        :param result_message:
        :return:
        """
        self.set_result(result, result_message)
        if "FAIL" in self.results_list:
            self.log.error("## {}: Test Case Failed".format(test_name))
            self.results_list.clear()
            assert True == False

        else:
            self.log.info("## {}: Test Case Successful".format(test_name))
            self.results_list.clear()
            assert True == True
