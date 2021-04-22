import unittest
from tests.home.login_test import LoginTests
from tests.courses.register_courses_multiple_data_set import RegisterCoursesTests

#get all tests from test classes

tc1 = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
tc2 = unittest.TestLoader().loadTestsFromTestCase(RegisterCoursesTests)

#create a test suite combining all test classes
smoke_test = unittest.TestSuite([tc1, tc2])

unittest.TextTestRunner(verbosity=2).run(smoke_test)