# -*- coding:utf-8 -*-

from app_tt.core import db, logger
from app_tt.engine.models import *

def record_book(info_book_dict):
    bk = get_book(info_book_dict['bookid'])

    if (bk != None):
        logger.warn("The book " + bk.title + " already exists in mbdb.")
        return
    
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
    pg = get_page(page_info_dict['bookid'], page_info_dict['page_num'])
    
    if (pg != None):
        logger.warn("The page " + pg.page_num + " from the book " + pg.book_id + " already exists in mbdb.")
        return
    
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
    pg_table = get_page_table_by_position(page_table_info_dict['pageid'], page_table_info_dict['top_pos'], page_table_info_dict['left_pos'], page_table_info_dict['right_pos'], page_table_info_dict['bottom_pos'])
    
    if (pg_table != None):
        logger.warn("The page table " + str(pg_table.id) + " from the book " + pg_table.book_id + " already exists in mbdb.")
        return
    
    pg_table = page_table(page_table_info_dict["bookid"],
              page_table_info_dict["pageid"],
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
    metadata_obj = get_metadata(metadata_info_dict['pagetableid'])
    
    if (metadata_obj != None):
        logger.warn("The metadata " + str(metadata_obj.id) + " from the page table " + str(metadata_obj.page_table_id) + " and the book " + metadata_obj.book_id + " already exists in mbdb.")
        return
    
    metadata_obj = metadata(metadata_info_dict["bookid"],
              metadata_info_dict["pageid"],
              metadata_info_dict["pagetableid"],
              metadata_info_dict["source"],
              metadata_info_dict["title"],
              metadata_info_dict["subtitle"],
              metadata_info_dict["subject"],
              metadata_info_dict["initial_date"],
              metadata_info_dict["final_date"])
    try:
        db.session.add(metadata_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def record_cell(cell_info_dict):
    cell_obj = get_cell_by_position(cell_info_dict['pagetableid'], cell_info_dict['x0'], cell_info_dict['y0'], cell_info_dict['x1'], cell_info_dict['y1'])
    
    if (cell_obj != None):
        logger.warn("The cell " + str(cell_obj.id) + " from the page table " + str(cell_obj.page_table_id) + " and the book " + cell_obj.book_id + " already exists in mbdb.")
        return
    
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
    workflow_transaction_obj = get_workflow_transaction(workflow_transaction_info_dict)
     
    if (workflow_transaction_obj != None):
        logger.warn("This workflow transaction already exists - Task 1 ID: " + str(workflow_transaction_obj.task_id_1) + ", Task 2 ID: " + str(workflow_transaction_obj.task_id_2) + ", Task 3 ID: " + str(workflow_transaction_obj.task_id_3) + ", Task 4 ID: " + str(workflow_transaction_obj.task_id_4) + ".")
        return

    workflow_transaction_obj = workflow_transaction(workflow_transaction_info_dict["task_id_1"], workflow_transaction_info_dict["task_id_2"], workflow_transaction_info_dict["task_id_3"], workflow_transaction_info_dict["task_id_4"])
     
    try:
        db.session.add(workflow_transaction_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update_workflow_transaction_t2(workflow_transaction_info_dict):
    workflow_transaction_obj = get_workflow_transaction_by_task_id_1(workflow_transaction_info_dict['task_id_1'])
     
    if (workflow_transaction_obj == None):
        logger.warn("Updating a workflow transaction that doesn't exist - Task 1 ID: " + str(workflow_transaction_info_dict['task_id_1']) + ", Task 2 ID: " + str(workflow_transaction_info_dict['task_id_2']) + ", Task 3 ID: " + str(workflow_transaction_info_dict['task_id_3']) + ", Task 4 ID: " + str(workflow_transaction_info_dict['task_id_4']) + ".")
        return
    
    workflow_transaction_obj.task_id_2 = workflow_transaction_info_dict['task_id_2']
        
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def update_workflow_transaction_t3(workflow_transaction_info_dict):
    workflow_transaction_obj = get_workflow_transaction_by_task_id_2(workflow_transaction_info_dict['task_id_2'])
     
    if (workflow_transaction_obj == None):
        logger.warn("Updating a workflow transaction that doesn't exist - Task 1 ID: " + str(workflow_transaction_info_dict['task_id_1']) + ", Task 2 ID: " + str(workflow_transaction_info_dict['task_id_2']) + ", Task 3 ID: " + str(workflow_transaction_info_dict['task_id_3']) + ", Task 4 ID: " + str(workflow_transaction_info_dict['task_id_4']) + ".")
        return
    
    workflow_transaction_obj.task_id_3 = workflow_transaction_info_dict['task_id_3']
        
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def update_workflow_transaction_t4(workflow_transaction_info_dict):
    workflow_transaction_obj = get_workflow_transaction_by_task_id_3(workflow_transaction_info_dict['task_id_3'])
     
    if (workflow_transaction_obj == None):
        logger.warn("Updating a workflow transaction that doesn't exist - Task 1 ID: " + str(workflow_transaction_info_dict['task_id_1']) + ", Task 2 ID: " + str(workflow_transaction_info_dict['task_id_2']) + ", Task 3 ID: " + str(workflow_transaction_info_dict['task_id_3']) + ", Task 4 ID: " + str(workflow_transaction_info_dict['task_id_4']) + ".")
        return
    
    workflow_transaction_obj.task_id_4 = workflow_transaction_info_dict['task_id_4']
        
    try:
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
        db.session.query(book).filter(book.id == book_id).delete(synchronize_session='fetch')
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def delete_workflow_transaction(workflow_transaction_info):
    try:
        db.session.query(workflow_transaction).filter(db.and_(workflow_transaction.task_id_1 == workflow_transaction_info['task_id_1'], workflow_transaction.task_id_2 == workflow_transaction_info['task_id_2'], workflow_transaction.task_id_3 == workflow_transaction_info['task_id_3'], workflow_transaction.task_id_4 == workflow_transaction_info['task_id_4'])).delete(synchronize_session='fetch')
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def delete_workflow_transactions(t1_ids):
    try:
        db.session.query(workflow_transaction).filter(workflow_transaction.task_id_1.in_(t1_ids)).delete(synchronize_session='fetch')
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e   

def get_book(book_id):
    return db.session.query(book).filter(book.id == book_id).first()

def get_page(book_id, page_num):
    return db.session.query(page).filter(db.and_(page.book_id == book_id, page.page_num == str(page_num))).first()

def get_page_table(book_id, page_id):
    return db.session.query(page_table).filter(db.and_(page_table.book_id == book_id, page_table.page_id == page_id)).all()

def get_page_table_by_position(page_id, top_pos, left_pos, right_pos, bottom_pos):
    return db.session.query(page_table).filter(db.and_(page_table.page_id == page_id, page_table.top_pos == top_pos, page_table.left_pos == left_pos, page_table.right_pos == right_pos, page_table.bottom_pos == bottom_pos)).first()

def get_page_table_by_local_url(page_id, local_url):
    results = db.session.query(page_table).filter(page_table.page_id == page_id).all()
    
    for result in results:
        if result.local_url in local_url:
            return result
    return None

def get_metadata(page_table_id):
    return db.session.query(metadata).filter(metadata.page_table_id == page_table_id).first()

def get_cell(page_table_id):
    return db.session.query(cell).filter(cell.page_table_id == page_table_id).all()

def get_cell_by_position(page_table_id, x0, y0, x1, y1):
    return db.session.query(cell).filter(db.and_(cell.page_table_id == page_table_id, cell.x0 == x0, cell.y0 == y0, cell.x1 == x1, cell.y1 == y1)).first()

def get_workflow_transaction(workflow_transaction_info=None):
    if (workflow_transaction_info == None):
        return db.session.query(workflow_transaction).all()
    else:
        return db.session.query(workflow_transaction).filter(db.and_(workflow_transaction.task_id_1 == workflow_transaction_info['task_id_1'], workflow_transaction.task_id_2 == workflow_transaction_info['task_id_2'], workflow_transaction.task_id_3 == workflow_transaction_info['task_id_3'], workflow_transaction.task_id_4 == workflow_transaction_info['task_id_4'])).first()

def get_workflow_transaction_by_task_id_1(task_id_1):
    return db.session.query(workflow_transaction).filter(workflow_transaction.task_id_1 == task_id_1).first()

def get_workflow_transaction_by_task_id_2(task_id_2):
    return db.session.query(workflow_transaction).filter(workflow_transaction.task_id_2 == task_id_2).first()

def get_workflow_transaction_by_task_id_3(task_id_3):
    return db.session.query(workflow_transaction).filter(workflow_transaction.task_id_3 == task_id_3).first()
