from app_tt.core import pbclient

def delete_app(short_name):
    for i in range(1,5):
        apps = pbclient.find_app(short_name="%s_tt%d" % (short_name, i))
        
        if (len(apps) == 0):
            return
        
        tt_app = apps[0]
        pbclient.delete_app(tt_app.id)