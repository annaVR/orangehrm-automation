"""
Util class
All most commonly used utilities should be implemented in this class
Example:
    name = self.util.get_unique_name()
"""

import time
import datetime
import traceback
import random, string
import utilities.custom_logger as cl
import logging

class Util(object):

    log = cl.CustomLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of seconds
        :param sec:
        :param info:
        :return:
        """
        if info is not None:
            self.log.info("Wait {} seconds for {}".format(sec, info))
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def get_alpha_numeric(self, length, type="letters"):
        """
        Get random string of characters

        :param length:
        :param type: Defaulted to 'letters'. Provide lower/upper/digits for different types
        :return: Returned random string of characters of specified parameters
        """
        alpha_num = ""
        if type.lower() == "lower":
            case = string.ascii_lowercase
        elif type.lower() == "upper":
            case = string.ascii_uppercase
        elif type.lower() == "digits":
            case = string.digits
        elif type.lower() == "mix":
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def get_unique_name_alpha_lower(self, char_count=10):
        """
        Get a unique name - alpha lower only. Wrapper for get_alpha_numeric() method
        :param char_count:
        :return:
        """
        return self.get_alpha_numeric(char_count, "lower")

    def get_unique_name_list(self, list_size = 5, item_length=None):
        """
        Get a list of names
        :param list_size: Number of names that needs to be returned. Defaults to 5.
        :param item_length: It should be a list containing numbers. Length of the list equals to the list_size.
        This determines the length of the each item in the list. Exapmles with Default length = 5: [5, 5, 5, 5, 5]
        or [4, 2, 3, 1, 4]
        :return:
        """
        names_list = []
        for i in range(0, list_size):
            names_list.append(self.get_unique_name_alpha_lower(item_length[i]))
        return names_list

    def verify_text_contains(self, actual_text, expected_text):
        """
        Verify actual text contains expected text string
        :param actual_text: Actual Text
        :param expected_text: Expected Text
        :return: True or False
        """
        self.log.info("Actual Text From Application Web UI: {}".format(actual_text))
        self.log.info("Expected Text: {}".format(expected_text))
        if expected_text.lower() in actual_text.lower():
            self.log.info("## Verification Successful: Expected Text IN Actual Text")
            return True
        else:
            self.log.error("## Verification Failed: Expected Text NOT IN Actual Text")
            return False

    def verify_text_match(self, actual_text, expected_text):
        """
        Verify actual text matches expected text string
        :param actual_text: Actual Text
        :param expected_text: Expected Text
        :return: True or False
        """
        self.log.info("Actual Text From Application Web UI: {}".format(actual_text))
        self.log.info("Expected Text From Application Web UI: {}".format(expected_text))
        if actual_text.lower() == expected_text.lower():
            self.log.info("## Verification Successful:  Actual Text MATCHES Expected Text")
            return True
        else:
            self.log.error("## Verification Failed: Actual Text DOES NOT MATCH Expected Text")
            return False

    def verify_list_match(self, expected_list, actual_list):
        """
        Verify if 2 list match.
        :param expected_list:
        :param actual_list:
        :return: True or False
        """
        return set(expected_list) == set(actual_list)

    def verify_list_contains(self, expected_list, actual_list):
        """
        Verify actual list contains elements of expected list
        :param expected_list:
        :param actual_list:
        :return: True or False
        """
        length = len(expected_list)
        for i in range(0, length):
            if expected_list[i] not in actual_list:
                return False
            else:
                return True


