# -*- coding: utf-8 -*-

from app_tt.data_mngr import data_manager2 as data_mngr2
from app_tt.core import logger
import app_tt.pb_apps.tt_apps.priority_task_manager as subject_table_map

import tempfile, os, sys
import math

"""
 
 1. recupera conteudo do mbdb
 2. cria arquivo de metadados com os respectivos
    campos de metadados para indexacao particular
    desses campos no doc do lucene
 3. chama o lucene e indexa o doc
 4. cria arquivo de conteudo com o campo de content
    para indexar no doc do lucene 
 5. chama o lucene e indexa o doc
 
"""

MAX_THRESHOLD = 5

class CSV_Generator:
    
    def __init__(self):
        self.lines_created_dict = {}
        self.columns_created_dict = {}
    
    def generate_metadata_file(self, metadata_dict, bookid):
        try:
            tmp_file = tempfile.mkstemp()
            f = open(tmp_file[1], "aw")
            
            f.write("Título: " + metadata_dict["title"] + "\n")
            f.write("Subtítulo: " + metadata_dict["subtitle"] + "\n")
            f.write("Assunto: " + subject_table_map.get_subject(metadata_dict["subject"]) + "\n")
            f.write("Fontes: " + metadata_dict["source"] + "\n")
            f.write("Título do Livro: " + metadata_dict["book_title"] + "\n")
            f.write("Página do Livro: " + str(metadata_dict["page_number"]) + "\n")
            f.write("Número da Tabela: " + str(metadata_dict["table_number"]) + "\n")
            
            f.close()
    
            f = open(tmp_file[1], "rb")
            data_mngr2.record_metadata_file(dict(
                                             book_id=bookid,
                                             page_number=metadata_dict["page_number"],
                                             table_number=metadata_dict["table_number"],
                                             mt_file=f.read()
                                             ))
            
            f.close()
            os.unlink(f.name)
            
            msg = "Metadata file generated with success. Content: " + str(metadata_dict)
            logger.info(msg)
        
        except Exception as e:
            logger.error(e)
            raise e
        
    
    def generate_data_file(self, cells_coordinates_list, maxX, maxY, cells_contents_list):
        #try:
            tmp_file = tempfile.mkstemp()
            f = open(tmp_file[1], "aw")
            
        #except Exception as e:
        #    logger.error(e)
        #    raise e
        
    
    def generate_csv(cells_coordinates_list, cells_contents_list):
        pass
            
    
    def create_lines(self, cells_coordinates_list):
        """
          Modify the cells bigger than the line height,
          splitting them into two cells of different heights.
        """
        
        global MAX_THRESHOLD
        
        lines_dict = self.group_cells_in_lines(cells_coordinates_list)
        
        print "lines_dict: " + str(lines_dict)
        
        lines_keys_sorted = lines_dict.keys()
        lines_keys_sorted.sort()
        
        for i in range(len(lines_dict.keys())):
            j = i + 1
            
            line_heigth = None
            if len(lines_dict.keys()) == j:
                line_height = sys.maxint
            else:
                line_height = lines_keys_sorted[j] - lines_keys_sorted[i]
            
            print "line_height: " + str(line_height)
            
            for cell in lines_dict[lines_dict.keys()[i]]:
                cond1 = cell[3] - cell[1] > line_height + MAX_THRESHOLD
                cond2 = cell[3] - cell[1] > line_height
                if cond1 and not cond2:
                    cell1 = [cell[0], cell[1], cell[2], line_height] 
                    cell2 = [cell[0], cell[1] + line_height , cell[2], cell[3]]
                    
                    print "cell1: " + str(cell1)
                    print "cell2: " + str(cell2)
                    
                    self.__append_cell_to_lines_dict(cell1)
                    self.__append_cell_to_lines_dict(cell2)
                elif cond2:
                    cell1 = [cell[0], cell[1], cell[2], line_height] 
                    cell2 = [cell[0], cell[1] + line_height , cell[2], cell[3]]
                    
                    print "cell1: " + str(cell1)
                    print "cell2: " + str(cell2)
                    
                    self.__append_cell_to_lines_dict(cell1)
                    self.__append_cell_to_lines_dict(cell2)
                else:
                    print "cell: " + str(cell)
                    self.__append_cell_to_lines_dict(cell)
                
                print "self.lines_created_dict: " + str(self.lines_created_dict)
                print "--------------"
        
        
    def create_columns(self, cells_coordinates_list):
        columns = self.group_cells_in_columns(cells_coordinates_list)
        
        for cell in columns:
            new_columns_dict = process_column(columns[i])
            
            for key in new_columns_dict.keys():
                columns[key] = new_columns_dict[key]
        
        return columns
    
    
    def group_cells_in_lines(self, cells_coordinates_list):
        lines_dict = {}
        for cell in cells_coordinates_list:
            line_y = self.__check_line_threshold_to_cell(cell, lines_dict)
            if lines_dict.has_key(cell[1]):
                lines_dict[cell[1]].append(cell)
            elif line_y != -1:
                lines_dict[line_y].append(cell)
            else:
                lines_dict[cell[1]] = [cell]
        
        return lines_dict
    
    
    def __check_line_threshold_to_cell(self, cell, lines_dict):
        """
          Verify if there is a line to the cell considering
          the threshold
        """
    
        global MAX_THRESHOLD
        
        for line_y in lines_dict.keys():
            #print "line_y: " + str(line_y)
            #print "cell: " + str(cell)
            #print "abs(line_y - cell[1]): " + str(abs(line_y - cell[1]))
            #print "------"
            if abs(line_y - cell[1]) <= MAX_THRESHOLD:
                return line_y
        
        return -1
        
        
    def group_cells_in_columns(self, cells_coordinates_list):
        MAX_THRESHOLD = 5
        columns_dict = {}
        for cell in cells_coordinates_list:
            if columns_dict.has_key(cell[0]):
                columns_dict[cell[0]].append(cell)
            else:
                columns_dict[cell[0]] = [cell]
        
        return columns_dict
        
        
    def __append_cell_to_lines_dict(self, cell):
        if self.lines_created_dict.has_key(cell[1]):
            self.lines_created_dict[cell[1]].append(cell)
        else:
            self.lines_created_dict[cell[1]] = [cell]
            
    
    def __append_cell_to_columns_dict(self, cell):
        if self.columns_created_dict.has_key(cell[0]):
            self.columns_created_dict[cell[0]].append(cell)
        else:
            self.columns_created_dict[cell[0]] = [cell]  
    