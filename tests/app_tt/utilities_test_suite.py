
import tests.app_tt.meb_util_test as meb_util_test
import tests.app_tt.pagination_test as pagination_test

import unittest

if __name__ == "__main__" :
    suite_meb_util = meb_util_test.suite()
    suite_pagination = pagination_test.suite()
     
    alltests = unittest.TestSuite([
                                    suite_meb_util,
                                    suite_pagination
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)
