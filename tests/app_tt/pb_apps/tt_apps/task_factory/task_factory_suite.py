

import tests.app_tt.pb_apps.tt_apps.task_factory_test_1 as task_factory_test_1
import tests.app_tt.pb_apps.tt_apps.task_factory_test_2 as task_factory_test_2
import tests.app_tt.pb_apps.tt_apps.task_factory_test_3 as task_factory_test_3
import tests.app_tt.pb_apps.tt_apps.task_factory_test_4 as task_factory_test_4

import unittest

if __name__ == "__main__" :
    suite_task_fact1 = task_factory_test_1.suite()
    suite_task_fact2 = task_factory_test_2.suite()
    suite_task_fact3 = task_factory_test_3.suite()
    suite_task_fact4 = task_factory_test_4.suite()
    
    alltests = unittest.TestSuite([
                                   suite_task_fact1,
                                   suite_task_fact2,
                                   suite_task_fact3,
                                   suite_task_fact4
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)