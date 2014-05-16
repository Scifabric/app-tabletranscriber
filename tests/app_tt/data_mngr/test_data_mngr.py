from app_tt.data_mngr import data_manager as data_mngr
import unittest
from unittest import TestCase


class test_data_mngr(TestCase):

    def setUp(self):
        # implementar remocao de objetos do modelo no data manager
        pass

    def test_book_insertion(self):
        info_book = dict(bookid="book_name_test", title="title_test", publisher="publisher_test", contributor="contributor_test", volume="volume_test", img="img_test")
        
        try:
            data_mngr.record_book(info_book)
        except Exception as e:
            print e
            raise AssertionError("Book insertion failed")

    def test_page_insertion(self):
        pass
    
    def test_cell_insertion(self):
        pass

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_data_mngr)
    return suite


if __name__ == "__main__":
    unittest.main()
