from app_tt.core import pbclient
from app_tt.meb_util import get_archive_book_data
from app_tt.data_mngr import data_manager as data_mngr
import json
import requests

def delete_app(short_name):
    for i in range(1,5):
        apps = pbclient.find_app(short_name="%s_tt%d" % (short_name, i))
        
        if (len(apps) == 0):
            return
        
        tt_app = apps[0]
        pbclient.delete_app(tt_app.id)
        
def delete_book(book_id):
    data_mngr.delete_book(book_id)
        
def create_tt_apps(app, short_name):
    o = app.get("/api/%s/init" % short_name)
    return o

def create_and_close_t1(app, short_name):
    o = app.get("/api/%s/init_and_close_t1" % short_name)
    return o

def get_book_data(book_id):
    return get_archive_book_data(book_id)

def authenticate_fb_user(base_url):
    auth = dict(facebook_user_id="12345", email="email@teste", name="fb-teste", full_name="fb-teste-fullname")
    r = requests.post(base_url + "/api/user/authenticate_facebook_user", data=json.dumps(auth), headers={'dataType': 'json', 'content-type': 'application/json'})
    print("Authenticate a FB User: " + json.loads(r.text)['response'])
    return auth

def submit_answer(base_url, task_run):
    r = requests.post(base_url + "/api/taskrun", data=json.dumps(task_run), headers={'dataType': 'json', 'content-type': 'application/json'})
    print(r)
    