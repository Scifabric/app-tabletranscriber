from tests.app_tt.base import add_book, add_page, add_page_table, add_cell, add_metadata, add_workflow_transaction, delete_workflow_transaction, delete_book, get_book, get_page, get_page_table, get_cell, get_metadata, get_workflow_transaction
import unittest
from unittest import TestCase
import datetime

class test_data_mngr(TestCase):
    
    def setUp(self):
        self.book_info = dict(bookid="book_name_test", title="title_test", publisher="publisher_test", contributor="contributor_test", volume="volume_test", img="img_test")
        self.page_info = dict(bookid=self.book_info['bookid'], archiveURL="www.test.com", page_num="10")
        self.page_table_info = dict(bookid=self.book_info['bookid'], pageid=0, initialDate=datetime.datetime.now(), finalDate=datetime.datetime.now(), local_url="www.teste.com", top_pos=0, left_pos=0, right_pos=500, bottom_pos=800)
        self.cell_info = dict(bookid=self.book_info['bookid'], pageid=0, pagetableid=0, text="text_test", x0=0, y0=0, x1=200, y1=300)
        self.metadata_info = dict(bookid=self.book_info['bookid'], pageid=0, pagetableid=0, source="source_test", footer="footer_test", title="title_test", subtitle="subtitle_test", subject="subject_test")
        self.workflow_transaction_info = dict(task_id_1="123", task_id_2=None, task_id_3=None, task_id_4=None)

    def tearDown(self):
        delete_book(self.book_info['bookid'])
        delete_workflow_transaction(self.workflow_transaction_info)

    def add_book(self, info_book):
        try:
            add_book(info_book)
        except Exception as e:
            print e
            raise AssertionError("Book insertion failed")
        
    def add_page(self, info_page):
        try:
            add_page(info_page)
        except Exception as e:
            print e
            raise AssertionError("Page insertion failed")
    
    def add_page_table(self, info_page_table):
        try:
            add_page_table(info_page_table)
        except Exception as e:
            print e
            raise AssertionError("Page Table insertion failed")
        
    def add_metadata(self, info_metadata):
        try:
            add_metadata(info_metadata)
        except Exception as e:
            print e
            raise AssertionError("Metadata insertion failed")        

    def add_cell(self, info_cell):
        try:
            add_cell(info_cell)
        except Exception as e:
            print e
            raise AssertionError("Cell insertion failed")
    
    def add_workflow_transaction(self, info_workflow_transaction):
        try:
            add_workflow_transaction(info_workflow_transaction)
        except Exception as e:
            print e
            raise AssertionError("Workflow Transaction insertion failed")    
    
    def test_book_insertion(self):
        # add a book
        self.add_book(self.book_info)
        self.assertTrue(get_book(self.book_info['bookid']))

    def test_page_insertion(self):
        self.add_book(self.book_info)
        # add a page
        self.add_page(self.page_info)
        self.assertTrue(get_page(self.page_info['bookid'], self.page_info['page_num']))
    
    def test_page_table(self):
        self.add_book(self.book_info)
        self.add_page(self.page_info)
        
        #add a page table
        page = get_page(self.page_info['bookid'], self.page_info['page_num'])
        self.page_table_info['pageid'] = page.id
        self.add_page_table(self.page_table_info)
        self.assertTrue(get_page_table(self.page_table_info['bookid'], self.page_table_info['pageid']))
        
    
    def test_metadata_insertion(self):
        self.add_book(self.book_info)
        self.add_page(self.page_info)

        page = get_page(self.page_info['bookid'], self.page_info['page_num'])
        self.page_table_info['pageid'] = page.id
        
        self.add_page_table(self.page_table_info)
        
        page_table = get_page_table(self.page_info['bookid'], self.page_table_info['pageid'])
        self.metadata_info['pageid'] = page.id
        self.metadata_info['pagetableid'] = page_table[0].id
        
        self.add_metadata(self.metadata_info)
        self.assertTrue(get_metadata(self.page_table_info['bookid'], self.page_table_info['pageid'], self.metadata_info['pagetableid']))
        
    
    def test_cell_insertion(self):
        self.add_book(self.book_info)
        self.add_page(self.page_info)

        page = get_page(self.page_info['bookid'], self.page_info['page_num'])
        self.page_table_info['pageid'] = page.id
        
        self.add_page_table(self.page_table_info)
        
        page_table = get_page_table(self.page_info['bookid'], self.page_table_info['pageid'])
        self.cell_info['pageid'] = page.id
        self.cell_info['pagetableid'] = page_table[0].id
        
        self.add_cell(self.cell_info)
        self.assertTrue(get_cell(self.page_table_info['bookid'], self.page_table_info['pageid'], self.cell_info['pagetableid']))
        
    def test_workflow_transation_insertion(self):
        self.add_workflow_transaction(self.workflow_transaction_info)
        self.assertTrue(get_workflow_transaction(self.workflow_transaction_info))
        

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_data_mngr)
    return suite


if __name__ == "__main__":
    unittest.main()
