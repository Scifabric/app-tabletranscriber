

import tests.app_tt.pb_apps.tt_apps.tt1_task_test as tt1_task_test
import tests.app_tt.pb_apps.tt_apps.tt2_task_test as tt2_task_test
import tests.app_tt.pb_apps.tt_apps.tt3_task_with_zoom_test as tt3_task_with_zoom_test
import tests.app_tt.pb_apps.tt_apps.tt3_task_without_zoom_test as tt3_task_without_zoom_test
import tests.app_tt.pb_apps.tt_apps.tt4_task_test as tt4_task_test

import unittest

if __name__ == "__main__" :
    suite_tt1 = tt1_task_test.suite()
    suite_tt2 = tt2_task_test.suite()
    suite_tt3_wz = tt3_task_with_zoom_test.suite()
    suite_tt3_woz = tt3_task_without_zoom_test.suite()
    suite_tt4 = tt4_task_test.suite()
    
    alltests = unittest.TestSuite([
                                   suite_tt1,
                                   suite_tt2,
                                   suite_tt3_wz,
                                   suite_tt3_woz,
                                   suite_tt4
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)