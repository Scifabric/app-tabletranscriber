
import tests.app_tt.pb_apps.tt_apps.tt_tasks.tt1_task_test as tt1_task_test
import tests.app_tt.pb_apps.tt_apps.tt_tasks.tt2_task_test as tt2_task_test
import tests.app_tt.pb_apps.tt_apps.tt_tasks.tt3_task_with_zoom_test as tt3_task_with_zoom_test
import tests.app_tt.pb_apps.tt_apps.tt_tasks.tt3_task_without_zoom_test as tt3_task_without_zoom_test
import tests.app_tt.pb_apps.tt_apps.tt_tasks.tt4_task_test as tt4_task_test

import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_select_test as ttapps_select_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_meta_test as ttapps_meta_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_struct_test as ttapps_struct_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_transcribe_test as ttapps_transcribe_test

import tests.app_tt.pb_apps.tt_apps.task_factory.task_factory_test_1 as task_factory_test_1
import tests.app_tt.pb_apps.tt_apps.task_factory.task_factory_test_2 as task_factory_test_2
import tests.app_tt.pb_apps.tt_apps.task_factory.task_factory_test_3 as task_factory_test_3
import tests.app_tt.pb_apps.tt_apps.task_factory.task_factory_test_4 as task_factory_test_4

import unittest

if __name__ == "__main__" :
    suite_task_fact1 = task_factory_test_1.suite()
    suite_task_fact2 = task_factory_test_2.suite()
    suite_task_fact3 = task_factory_test_3.suite()
    suite_task_fact4 = task_factory_test_4.suite()
    
    suite_tt1 = tt1_task_test.suite()
    suite_tt2 = tt2_task_test.suite()
    suite_tt3_wz = tt3_task_with_zoom_test.suite()
    suite_tt3_woz = tt3_task_without_zoom_test.suite()
    suite_tt4 = tt4_task_test.suite()
    
    suite_ttapps_select = ttapps_select_test.suite()
    suite_ttapps_meta = ttapps_meta_test.suite()
    suite_ttapps_struct = ttapps_struct_test.suite()
    suite_ttapps_transcribe = ttapps_transcribe_test.suite() 
    
    alltests = unittest.TestSuite([
                                   suite_task_fact1,
                                   suite_task_fact2,
                                   suite_task_fact3,
                                   suite_task_fact4,
                                   suite_tt1,
                                   suite_tt2,
                                   suite_tt3_wz,
                                   suite_tt3_woz,
                                   suite_tt4,
                                   suite_ttapps_select,
                                   suite_ttapps_meta,
                                   suite_ttapps_struct,
                                   suite_ttapps_transcribe
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)
