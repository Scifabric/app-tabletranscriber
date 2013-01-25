import os
import app_tt.view.test_application as test_application
import app_tt.engine.test_api as test_api
import unittest

if __name__ == "__main__":
    suite_api = test_api.suite()
    suite_app = test_application.suite()
    alltests = unittest.TestSuite([suite_api, suite_app])

    result = unittest.TestResult()
    alltests.run(result, debug=True)

    if not result.wasSuccessful():
        print result.errors

