from app_tt.core import db

class book(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(255), unique=True)
    publisher = db.Column(db.String(255))
    contributor = db.Column(db.String(255))
    volume = db.Column(db.String(50))
    img_url = db.Column(db.String(255))
    #initialDate = db.Column(db.DateTime)
    #finalDate = db.Column(db.DateTime)
    
    def __init__(self, id, title=None, publisher=None, contributor=None, volume=None,\
                 img_url=None):
        self.id = id
        self.title = title
        self.publisher = publisher
        self.contributor = contributor
        self.volume = volume
        self.img_url = img_url 
        #self.initialDate = initialDate
        #self.finalDate = finalDate

    def __repr__(self):
        return '<book %r, %r , %r, %r, %r, %r>' % (self.id, self.title, self.publisher,\
                                                   self.contributor, self.volume,\
                                                    self.img_url)
 
class page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.String(100), db.ForeignKey('book.id'))
    archiveURL = db.Column(db.String(255), unique=True)
    page_num = db.Column(db.String(10))
    
    def __init__(self, bookid=None, archiveURL=None, page_num=None):
        self.book_id = bookid
        self.archiveURL = archiveURL
        self.page_num = page_num
        
    def __repr__(self):
        return '<page %r, %r, %r, %r>' % (self.id, self.book_id, self.archiveURL, self.page_num)


class page_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    book_id = db.Column(db.String(100), db.ForeignKey('book.id'))
    initialDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime, nullable=False)
    local_url = db.Column(db.String(255), nullable=False)
    top_pos = db.Column(db.Integer, nullable=False) 
    left_pos = db.Column(db.Integer, nullable=False)
    right_pos = db.Column(db.Integer, nullable=False)
    bottom_pos = db.Column(db.Integer, nullable=False)

    def __init__(self, bookid=None, pageid=None, initialDate=None, finalDate=None, local_url=None, top_pos=None, left_pos=None, right_pos=None, bottom_pos=None):
        self.book_id = bookid
        self.page_id = pageid
        self.initialDate = initialDate
        self.finalDate = finalDate
        self.local_url = local_url
        self.top_pos = top_pos
        self.left_pos = left_pos
        self.right_pos = right_pos
        self.bottom_pos = bottom_pos
        
    def __repr__(self):
        return '<page_table %r, %r, %r, %r, %r, %r, %r, %r, %r, %r>' % (self.id, self.book_id, self.page_id, self.initialDate, self.finalDate, self.local_url, self.top_pos, self.left_pos, self.right_pos, self.bottom_pos)

class metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_table_id = db.Column(db.Integer, db.ForeignKey('page_table.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    book_id = db.Column(db.String(100), db.ForeignKey('book.id'))
    source = db.Column(db.String(255))       
    footer = db.Column(db.String(255))        
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))        
    subject = db.Column(db.String(255))
    
    def __init__(self, book_id=None, page_id=None, page_table_id=None, source=None, footer=None, title=None, subtitle=None, subject=None):
        self.page_table_id = page_table_id
        self.page_id = page_id
        self.book_id = book_id
        self.source = source
        self.footer = footer
        self.title = title
        self.subtitle = subtitle
        self.subject = subject
        
    def __repr__(self):
        return '<metadata %r, %r, %r, %r, %r, %r, %r, %r, %r>' % (self.id, self.page_table_id, self.page_id, self.book_id, self.source, self.footer, self.title, self.subtitle, self.subject)  

class cell(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_table_id = db.Column(db.Integer, db.ForeignKey('page_table.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    book_id = db.Column(db.String(100), db.ForeignKey('book.id'))
    text = db.Column(db.String(255))
    x0 = db.Column(db.Integer, nullable=False)
    y0 = db.Column(db.Integer, nullable=False)
    x1 = db.Column(db.Integer, nullable=False)
    y1 = db.Column(db.Integer, nullable=False)
    
    def __init__(self, book_id=None, page_id=None, page_table_id=None, text=None, x0=None, y0=None, x1=None, y1=None):
        self.page_table_id = page_table_id
        self.page_id = page_id
        self.book_id = book_id
        self.text = text
        self.x0 = x0
        self.y0 = x0
        self.x1 = x1
        self.y1 = y1
        
    def __repr__(self):
        return '<cell %r, %r, %r, %r, %r, %r, %r, %r, %r>' % (self.id, self.page_table_id, self.page_id, self.book_id, self.text, self.x0, self.y0, self.x1, self.y1)

class workflow_transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id_1 = db.Column(db.Integer, nullable=False)
    task_id_2 = db.Column(db.Integer, nullable=False)
    task_id_3 = db.Column(db.Integer, nullable=True)   
    task_id_4 = db.Column(db.Integer, nullable=True)
    
    def __init__(self, task_id_1=None, task_id_2=None, task_id_3=None, task_id_4=None):
        self.task_id_1 = task_id_1
        self.task_id_2 = task_id_2
        self.task_id_3 = task_id_3
        self.task_id_4 = task_id_4
        
    def __repr__(self):
        return '<workflow_transaction %r, %r, %r, %r, %r>' % (self.id, self.task_id_1, self.task_id_2, self.task_id_3, self.task_id_4)

class report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    app_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime)

    def __init__(self, msg=None, a_id=None, t_id=None, u_id=None, ctd=None):
        self.message = msg
        self.app_id = a_id
        self.task_id = t_id
        self.user_id = u_id
        self.created = ctd
        
    def __repr__(self):
        return '<report %r, %r, %r, %r, %r, %r>' % (self.id, self.message,
                                           self.app_id, self.task_id,
                                           self.user_id, self.created)

    
#class fact(db.Model):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #user_id = db.Column(db.Integer) 
    #book_id = db.Column(db.String(100), Fore)
    
    