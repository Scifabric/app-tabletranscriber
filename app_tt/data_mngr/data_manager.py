# -*- coding:utf-8 -*-

from app_tt.core import db
from app_tt.engine.models import book

def record_book_info_mbdb(info_book):
    bk = book(info_book['bookid'],
              info_book['title'],
              info_book['publisher'],
              info_book['contributor'],
              info_book['volume'],
              info_book['img'])
    
    db.session.add(bk)
    db.session.commit()