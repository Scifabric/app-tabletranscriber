# -*- coding:utf-8 -*-

from app_tt.core import db, logger
from app_tt.engine.models import *

def record_book(info_book_dict):
    bk = book.query.filter_by(id=info_book_dict['bookid']).first()

    if (bk != None):
        logger.info("The book " + bk.title + " already exists in mbdb.")
        raise
    
    bk = book(info_book_dict['bookid'],
              info_book_dict['title'],
              info_book_dict['publisher'],
              info_book_dict['contributor'],
              info_book_dict['volume'],
              info_book_dict['img']) 
    try:
        db.session.add(bk)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def record_page(page_info_dict):
    pg = page(page_info_dict["bookid"],
              page_info_dict["archiveURL"],
              page_info_dict["page_num"])
    
    try:
        db.session.add(pg)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_page_table(page_table_info_dict):
    pg_table = page_table(page_table_info_dict["bookid"],
              page_table_info_dict["pageid"],
              page_table_info_dict["initialDate"],
              page_table_info_dict["finalDate"],
              page_table_info_dict["local_url"],
              page_table_info_dict["top_pos"],
              page_table_info_dict["left_pos"],
              page_table_info_dict["right_pos"],
              page_table_info_dict["bottom_pos"])
    try:
        db.session.add(pg_table)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_metadata(metadata_info_dict):
    metadata_obj = metadata(metadata_info_dict["bookid"],
              metadata_info_dict["pageid"],
              metadata_info_dict["pagetableid"],
              metadata_info_dict["source"],
              metadata_info_dict["footer"],
              metadata_info_dict["title"],
              metadata_info_dict["subtitle"],
              metadata_info_dict["subject"])
    try:
        db.session.add(metadata_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_cell(cell_info_dict):
    cell_obj = cell(cell_info_dict["bookid"],
              cell_info_dict["pageid"],
              cell_info_dict["pagetableid"],
              cell_info_dict["text"],
              cell_info_dict["x0"],
              cell_info_dict["y0"],
              cell_info_dict["x1"],
              cell_info_dict["y1"])
    try:
        db.session.add(cell_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_workflow_transaction(workflow_transaction_info_dict):
    workflow_transaction_obj = workflow_transaction(workflow_transaction_info_dict["task_id_1"],
              workflow_transaction_info_dict["task_id_2"],
              workflow_transaction_info_dict["task_id_3"],
              workflow_transaction_info_dict["task_id_4"])
    try:
        db.session.add(workflow_transaction_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_report(infos):
    r = report(infos['msg'], 
               infos['app_id'],
               infos['task_id'], 
               infos['user_id'], 
               infos['created']) 
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e     
    
def delete_book(book_id):
    try:
        db.session.query(book).filter(book.id == book_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def delete_workflow_transaction(workflow_transaction_info):
    try:
        db.session.query(workflow_transaction).filter(workflow_transaction.task_id_1 == workflow_transaction_info['task_id_1'] and workflow_transaction.task_id_2 == workflow_transaction_info['task_id_2'] and workflow_transaction.task_id_3 == workflow_transaction_info['task_id_3'] and workflow_transaction.task_id_4 == workflow_transaction_info['task_id_4']).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e   

def get_book(book_id):
    return db.session.query(book).filter(book.id == book_id).first()

def get_page(book_id, page_num):
    return db.session.query(page).filter(page.book_id == book_id and book.page_num == page_num).first()

def get_page_table(book_id, page_id):
    return db.session.query(page_table).filter(page_table.book_id == book_id and page_table.page_id == page_id)

def get_metadata(book_id, page_id, page_table_id):
    return db.session.query(metadata).filter(metadata.book_id == book_id and metadata.page_id == page_id and metadata.page_table_id == page_table_id)

def get_cell(book_id, page_id, page_table_id):
    return db.session.query(cell).filter(cell.book_id == book_id and cell.page_id == page_id and cell.page_table_id == page_table_id)

def get_workflow_transaction(workflow_transaction_info):
    return db.session.query(workflow_transaction).filter(workflow_transaction.task_id_1 == workflow_transaction_info['task_id_1'] and workflow_transaction.task_id_2 == workflow_transaction_info['task_id_2'] and workflow_transaction.task_id_3 == workflow_transaction_info['task_id_3'] and workflow_transaction.task_id_4 == workflow_transaction_info['task_id_4'])


    