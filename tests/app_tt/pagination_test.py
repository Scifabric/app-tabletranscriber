# -*- coding: utf-8 -*-

from app_tt.pagination import Pagination 
from app_tt.meb_exceptions.meb_exception import Meb_pagination_exception

import unittest

class pagination_test(unittest.TestCase):
    
    def setUp(self):
        self.p1 = Pagination(1, 10, 70) 
    
    # testing functions

    def test_init_01(self):
        try:
            p1 = Pagination(0, 0, 0)
            assert False

        except Meb_pagination_exception as e:
            self.assertEquals(e.code, 1) 
    
    def test_init_02(self):
        try:
            p1 = Pagination(1, 0, 0)
            assert False

        except Meb_pagination_exception as e:
            self.assertEquals(e.code, 2) 
    
    def test_init_03(self):
        try:
            p1 = Pagination(1, 5, 0)
            assert False

        except Meb_pagination_exception as e:
            self.assertEquals(e.code, 3) 
    
    def test_pages_01(self):
        try:
            self.assertEquals(self.p1.pages, 7)
        except Exception as e:
            print e
            assert False
    
    def test_has_prev_01(self):
        try:
            self.assertFalse(self.p1.has_prev)
            
            p2 = Pagination(3,1,10)
            self.assertTrue(p2.has_prev)
            
        except Exception as e:
            print e
            assert False
    
    def test_has_next_01(self):
        try:
            self.assertTrue(self.p1.has_next)
            
            p2 = Pagination(10, 5, 10)
            self.assertFalse(p2.has_next)
        except Exception as e:
            print e
            assert False
    
    def test_iter_page_01(self):
        try:
            self.p1.iter_pages()
            
            self.assertTrue(self.p1.page, 2)
            self.assertTrue(self.p1.per_page, 10)
            self.assertTrue(self.p1.total_count, 70)
            
            self.p1.iter_pages()
            
            self.assertTrue(self.p1.page, 3)
            self.assertTrue(self.p1.per_page, 10)
            self.assertTrue(self.p1.total_count, 70)
            
        except Exception as e:
            print e
            assert False

    def test_iter_page_02(self):
        try:
            p2 = Pagination(1, 6, 60)
            
            for i in range(1, 61):
                self.assertTrue(p2.page, i)
                self.assertTrue(p2.per_page, 6)
                self.assertTrue(p2.total_count, 60)
                
                result = p2.iter_pages()
                self.assertNotEqual(result, None)
            
        except Exception as e:
            print e
            assert False    
    
    def test_iter_page_03(self):
        try:
            p2 = Pagination(1, 6, 10)
            
            for i in range(1, 11):
                self.assertTrue(p2.page, i)
                self.assertTrue(p2.per_page, 6)
                self.assertTrue(p2.total_count, 10)
                
                p2.iter_pages()
            
        except Exception as e:
            print e 
            assert False
    
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(pagination_test)
    return suite
    
if __name__ == '__main__':
    unittest.main()

