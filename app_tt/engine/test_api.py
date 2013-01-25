from unittest import TestCase
import sys
import unittest
import app_tt.view.application as application
import api
import requests
import json
import pbclient
import app_tt.default_settings as settings

class test_api(TestCase):


    def setUp(self):
        app = application.app
        app.config['TESTING'] = True
        self.app = app.test_client()
        pbclient.set('endpoint', settings.PYBOSSA_URL)
        pbclient.set('api_key', settings.API_KEY)
        
        try:
            pybossa_api = requests.get(settings.PYBOSSA_URL + "/api")
        except:
            raise AssertionError("Pybossa's not working")
        if not pybossa_api.content:
            raise AssertionError("Pybossa's api is not working")

    def test_00_init(self):
        # Creating new tt applications
        pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
        if len(pb_app) == 0:
            self.app.get("/api/custodevida1946bras/init")
            pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
            
            self.assertTrue(len(pb_app) > 0, "Error tt_app was not created")
        
        else:   # application is already created
            n_app_tasks = len(pbclient.get_tasks(pb_app[0].id, sys.maxint))
            rv = self.app.get("/api/custodevida1946bras/init")

            self.assertTrue(rv.data, "Error tt_app was not created")
            
            # if application is already created init cant duplicate the tasks
            self.assertEqual(n_app_tasks,
                    len(pbclient.get_tasks(pb_app[0].id, sys.maxint)),
                    "Error duplicated tasks")


    def test_01_init(self):
        # Creating tt_app where book_id does not exist
        #self.app.get("/api/does_not_exist/init")
        return True

    def test_check_app_done(self):
        return True


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_api)
    return suite

if __name__ == "__main__":
    unittest.main()
