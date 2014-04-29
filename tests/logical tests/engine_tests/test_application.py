from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.base import delete_app
from app_tt.meb_util import archiveBookData 
import unittest
import app_tt.engine.tasks as engine
import os 

class test_application(TestCase):


    def setUp(self):
        app = application
        self.app = app.test_client()
        delete_app("estatisticasdodi1950depa")
    

    def new_ttapplications(self, short_name):
        o = self.app.get("/api/%s/init" % short_name)
        return o
    
    def bookdata(self, book_id):
        return engine.archiveBookData(book_id)


    def test_home(self):
        rv = self.app.get('/')
        assert "<h1>Mem&oacute;ria Estat&iacute;stica do Brasil</h1>" in rv.data


    def test_colabore(self):
        self.new_ttapplications('estatisticasdodi1950depa')
        pb_app = pbclient.find_app(short_name="estatisticasdodi1950depa_tt1")
        
        if len(pb_app) > 0:
            tt_app = pb_app[0]
            coll_request = self.app.get('/collaborate', follow_redirects=True)

            book_data = self.bookdata(tt_app.short_name[:-4])
            
            self.assertTrue(book_data["title"] in coll_request.data.decode("utf-8"),
                    "Error book title was not found in collaborate page")

            self.assertTrue(book_data["volume"] in coll_request.data.decode("utf-8"),
                    "Error book volume was not found in collaborate page")

            self.assertTrue(book_data["publisher"] in coll_request.data.decode("utf-8"),
                    "Error book publisher was not found in collaborate page")

            self.assertTrue(book_data["contributor"] in coll_request.data.decode("utf-8"),
                    "Error book contributor was not found in collaborate page" )

        else:
            raise AssertionError("Application was not created")


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_application)
    return suite


if __name__ == "__main__":
    unittest.main()
