# -*- coding: utf-8 -*-

from app_tt.meb_results.csv_generator import CSV_Generator
import app_tt.data_mngr.data_manager2 as data_mngr2

import unittest
import tempfile, os

class csv_generator_test(unittest.TestCase):
    
    def setUp(self):
        self.bookid = "bookid1"
        self.page_number = 123
        self.page_table_number = 2
        
        self.csv_generator = CSV_Generator()
        self.cells_coordinates = [
                                  [0, 0, 20, 30],
                                  [20, 0, 40, 30], 
                                  [40, 0, 60, 40],
                                  [0, 30, 20, 40],
                                  [20, 30, 40, 40],
                                  [0, 40, 20, 50],
                                  [20, 40, 40, 50],
                                  [40, 40, 60, 50]
                                 ]
        
        self.cells_coordinates_with_threshold = [
                                                 [0,0,20,30],
                                                 [20,0,40,30],
                                                 [40,0,60,40],
                                                 [0,25,20,45],
                                                 [20,30,40,45],
                                                 [0,40,20,50],
                                                 [20,45,40,50],
                                                 [40,40,60,50]
                                                 ]
        
    def tearDown(self):
        data_mngr2.delete_metadata_file(self.bookid, self.page_number, self.page_table_number)
        pass
    
    
    # testing functions
    
    def test_generate_metadata_file_01(self):
        metadata1 = dict(
                         title="title1", 
                         subtitle="subtitle1",
                         subject="0",
                         source="source1",
                         book_title="book_title1",
                         page_number=self.page_number,
                         table_number=self.page_table_number
                         )
         
        self.csv_generator.generate_metadata_file(metadata1, bookid=self.bookid)
         
        tmp_file = tempfile.mkstemp()
        f = open(tmp_file[1], 'wb')
        f.write(data_mngr2.get_metadata_file(self.bookid, self.page_number, self.page_table_number).mt_file)
        f.close()
         
        f = open(tmp_file[1], 'r')
        lines = f.readlines()
        f.close()
         
        os.unlink(tmp_file[1])
         
        self.assertEquals(unicode(lines[0], "utf-8"), u"Título: title1\n")
        self.assertEquals(unicode(lines[1], "utf-8"), u"Subtítulo: subtitle1\n")
        self.assertEquals(unicode(lines[2], "utf-8"), u"Assunto: Economia\n")
        self.assertEquals(unicode(lines[3], "utf-8"), u"Fontes: source1\n")
        self.assertEquals(unicode(lines[4], "utf-8"), u"Título do Livro: book_title1\n")
        self.assertEquals(unicode(lines[5], "utf-8"), u"Página do Livro: 123\n")
        self.assertEquals(unicode(lines[6], "utf-8"), u"Número da Tabela: 2\n")
         
     
    def test_group_cells_in_lines_01(self):
        new_lines = self.csv_generator.group_cells_in_lines(self.cells_coordinates)
         
        self.assertEquals(new_lines[0][0], [0,0,20,30])
        self.assertEquals(new_lines[0][1], [20,0,40,30])
        self.assertEquals(new_lines[0][2], [40,0,60,40])
        self.assertEquals(new_lines[30][0], [0,30,20,40])
        self.assertEquals(new_lines[30][1], [20,30,40,40])
        self.assertEquals(new_lines[40][0], [0,40,20,50])
        self.assertEquals(new_lines[40][1], [20,40,40,50])
        self.assertEquals(new_lines[40][2], [40,40,60,50])
                                   
    
    def test_group_cells_in_lines_02(self):
        new_lines = self.csv_generator.group_cells_in_lines(self.cells_coordinates_with_threshold)
        
        self.assertEquals(new_lines[0][0], [0,0,20,30])
        self.assertEquals(new_lines[0][1], [20,0,40,30])
        self.assertEquals(new_lines[0][2], [40,0,60,40])
        self.assertEquals(new_lines[25][0], [0,25,20,45])
        self.assertEquals(new_lines[25][1], [20,30,40,45])
        self.assertEquals(new_lines[40][0], [0,40,20,50])
        self.assertEquals(new_lines[40][1], [20,45,40,50])
        self.assertEquals(new_lines[40][2], [40,40,60,50])
     
    
    def test_group_cells_in_columns_01(self):
        new_columns = self.csv_generator.group_cells_in_columns(self.cells_coordinates)
         
        self.assertEquals(new_columns[0][0],  [0,0,20,30])
        self.assertEquals(new_columns[0][1],  [0,30,20,40])
        self.assertEquals(new_columns[0][2],  [0,40,20,50])
        self.assertEquals(new_columns[20][0], [20,0,40,30])
        self.assertEquals(new_columns[20][1], [20,30,40,40])
        self.assertEquals(new_columns[20][2], [20,40,40,50])
        self.assertEquals(new_columns[40][0], [40,0,60,40])
        self.assertEquals(new_columns[40][1], [40,40,60,50])
    
    
    def test_create_lines_01(self):
        self.csv_generator.create_lines(self.cells_coordinates)
        
        lines_created = self.csv_generator.lines_created_dict
        
        self.assertEquals(lines_created[0][0], [0,0,20,30])
        self.assertEquals(lines_created[0][1], [20,0,40,30])
        self.assertEquals(lines_created[0][2], [40,0,60,30])
        self.assertEquals(lines_created[30][0], [40,30,60,40])
        self.assertEquals(lines_created[30][1], [0,30,20,40])
        self.assertEquals(lines_created[30][2], [20,30,40,40])
        self.assertEquals(lines_created[40][0], [0,40,20,50])
        self.assertEquals(lines_created[40][1], [20,40,40,50])
        self.assertEquals(lines_created[40][2], [40,40,60,50])
        
        print "==================="
    
    def test_create_lines_02(self):
        self.csv_generator.create_lines(self.cells_coordinates_with_threshold)
        
        lines_created = self.csv_generator.lines_created_dict
        
        print "lines_created: " + str(lines_created)
        
        self.assertEquals(lines_created[0][0], [0,0,20,30])
        self.assertEquals(lines_created[0][1], [20,0,40,30])
        self.assertEquals(lines_created[0][2], [40,0,60,40])
        self.assertEquals(lines_created[25][0], [0,25,20,45])
        self.assertEquals(lines_created[25][1], [20,30,40,45])
        self.assertEquals(lines_created[25][2], [40,25,60,40])
        self.assertEquals(lines_created[40][0], [0,40,20,50])
        self.assertEquals(lines_created[40][1], [20,45,40,50])
        self.assertEquals(lines_created[40][2], [40,40,60,50])
    
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(csv_generator_test)
    return suite


if __name__ == '__main__':
    unittest.main()
        