
import tests.app_tt.pb_apps.apps_test as apps_test
import tests.app_tt.pb_apps.pb_task_test as pb_task_test

import unittest

if __name__ == "__main__" :
    
    suite_apps = apps_test.suite()
    suite_pb_task = pb_task_test.suite()
    
    alltests = unittest.TestSuite([
                                   suite_apps,
                                   suite_pb_task
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)
