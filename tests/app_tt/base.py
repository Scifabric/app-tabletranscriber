from app_tt.core import pbclient
import app_tt.engine.tasks as engine

def delete_app(short_name):
    for i in range(1,5):
        apps = pbclient.find_app(short_name="%s_tt%d" % (short_name, i))
        
        if (len(apps) == 0):
            return
        
        tt_app = apps[0]
        pbclient.delete_app(tt_app.id)
        
def create_tt_apps(app, short_name):
    o = app.get("/api/%s/init" % short_name)
    return o

def get_book_data(book_id):
    return engine.archiveBookData(book_id)