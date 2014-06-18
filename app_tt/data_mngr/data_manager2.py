from app_tt.core import db, logger
from app_tt.engine.models import *
from app_tt.meb_exceptions.meb_data_manager_exception import Meb_data_manager_metadata_file_exception


def record_metadata_file(metadata_file_dict):
    try:
        mt_file = metadata_file(
                                metadata_file_dict["book_id"],
                                metadata_file_dict["page_number"],
                                metadata_file_dict["table_number"],
                                metadata_file_dict["mt_file"]
                                )
        
        
        db.session.add(mt_file)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        
        logger.error(e)
        logger.error(Meb_data_manager_metadata_file_exception(1, 
                                                              metadata_file_dict["book_id"], 
                                                              metadata_file["page_number"], 
                                                              metadata_file["table_number"]
                                                             ))
        raise e



def delete_metadata_file(bookid, page_id, page_table_id):
    try:
    
        db.session.query(metadata_file).filter(metadata_file.book_id == bookid) \
            .filter(metadata_file.page_id == page_id) \
            .filter(metadata_file.page_table_id == page_table_id).delete()
        db.session.commit()
    
    except Exception as e:
        logger.error(e)
        db.session.rollback()
        raise e


def get_metadata_file(bookid, page_id, page_table_id):
    return db.session.query(metadata_file).filter(metadata_file.book_id == bookid) \
        .filter(metadata_file.page_id == page_id) \
        .filter(metadata_file.page_table_id == page_table_id).first()



def get_csv_file(csv_file_id):
    pass

def record_csv_file(csv_file):
    pass

def delete_csv_file(bookid, page_id, page_table_id):
    pass




