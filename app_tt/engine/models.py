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
    
#class fact(db.Model):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #user_id = db.Column(db.Integer) 
    #book_id = db.Column(db.String(100), Fore)
    
    