# -*- coding: utf-8 -*-

import app_tt.meb_util as meb_util
from app_tt.meb_exceptions.meb_exception import Archive_book_data_exception

import unittest


class MebUtil_TestCase(unittest.TestCase):
    
    # testing functions

    def test_get_archive_book_data_01(self):
        try:
            data = meb_util.get_archive_book_data("rpparaiba1918")
            
            self.assertEquals(data["bookid"], "rpparaiba1918")
            self.assertEquals(data["img"], "http://www.archive.org/download/rpparaiba1918/page/n7_w100_h100")
            self.assertEquals(data["title"], u"Mensagem apresentada à Assembléa Legislativa do Estado da Parahyba na abertura da 3a. sessão ordinaria da 8a. legislatura, a 1o. de setembro de 1918, pelo Dr. Francisco Camillo de Hollanda, presidente do Estado. (Vol. 1917)")
            self.assertEquals(data["publisher"], u"[Imprensa Oficial - Parahyba do Norte")
            self.assertEquals(data["contributor"], u"Biblioteca do Ministério da Fazenda no Rio de Janeiro")
            self.assertEquals(data["volume"], u"1917")
        except Exception as e:
            print e
            assert False
    
    def test_get_tt_images_01(self):
        try:
            book_id = "rpparaiba1918"
            imgs = meb_util.get_tt_images(book_id)
            
            self.assertTrue(len(imgs), 75)
            
            for i in range(0, 74):
                self.assertEquals(imgs[i]["url_m"], "http://www.archive.org/download/%s/page/n%d_w%d_h%d" % (book_id, i, 550, 700))
                self.assertEquals(imgs[i]["url_b"], "http://www.archive.org/download/%s/page/n%d" % (book_id, i))
            
        except Exception as e:
            print e
            assert False
    
    def test_get_tt_images_02(self):
        try:
            book_id = "rdi1821balano"
            imgs = meb_util.get_tt_images(book_id)
            
            self.assertTrue(len(imgs), 75)
            
            for i in range(0, 74):
                self.assertEquals(imgs[i]["url_m"], "http://www.archive.org/download/%s/page/n%d_w%d_h%d" % (book_id, i, 550, 700))
                self.assertEquals(imgs[i]["url_b"], "http://www.archive.org/download/%s/page/n%d" % (book_id, i))
            
        except Exception as e:
            print e
            assert False

if __name__ == '__main__':
    unittest.main()

