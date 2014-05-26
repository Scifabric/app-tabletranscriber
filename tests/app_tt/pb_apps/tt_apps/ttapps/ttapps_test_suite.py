
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_select_test as ttapps_select_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_meta_test as ttapps_meta_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_struct_test as ttapps_struct_test
import tests.app_tt.pb_apps.tt_apps.ttapps.ttapps_transcribe_test as ttapps_transcribe_test

import unittest

if __name__ == "__main__" :
    suite_ttapps_select = ttapps_select_test.suite()
    suite_ttapps_meta = ttapps_meta_test.suite()
    suite_ttapps_struct = ttapps_struct_test.suite()
    suite_ttapps_transcribe = ttapps_transcribe_test.suite() 
    
    alltests = unittest.TestSuite([
                                   suite_ttapps_select,
                                   suite_ttapps_meta,
                                   suite_ttapps_struct,
                                   suite_ttapps_transcribe
                                   ])

    unittest.TextTestRunner(verbosity=2).run(alltests)
