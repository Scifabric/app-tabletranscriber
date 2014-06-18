# -*- coding: utf-8 -*-

from app_tt.meb_exceptions.meb_exception import Meb_exception

class Meb_data_manager_metadata_file_exception( Meb_exception ):
    std_exception_msgs = {
           1 : "MEB-DATA-MANAGER-METADATA-FILE-1: Cannot record metadata file",
          }

    def __init__(self, exc_code, book_id, page_id, page_table_id):
        msg = self.config_msg(exc_code, book_id, page_id, page_table_id)
        super(Meb_data_manager_metadata_file_exception, self).__init__(exc_code, msg)
    
    def config_msg(self, exc_code, book_id, page_id, page_table_id):
        return "%s | book_id : %s | page_id: %d | table_id: %d" % (self.std_exception_msgs[exc_code], book_id, page_id, page_table_id)