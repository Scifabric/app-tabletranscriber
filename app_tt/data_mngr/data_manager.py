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

def get_book(book_id):
    return db.session.query(book).filter(book.id == book_id).first()
    