import os
import test_application
import test_api
import unittest

if __name__ == "__main__":
    suite_api = test_api.suite()
    suite_app = test_application.suite()
    alltests = unittest.TestSuite([suite_api, suite_app])

    unittest.TextTestRunner(verbosity=2).run(alltests)
