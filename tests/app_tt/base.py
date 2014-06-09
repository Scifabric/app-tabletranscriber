from app_tt.core import pbclient
from app_tt.meb_util import get_archive_book_data
from app_tt.data_mngr import data_manager as data_mngr
import json
import requests

# Data Manager functions        
def delete_book(book_id):
    data_mngr.delete_book(book_id)
    
def add_book(info_book):
    data_mngr.record_book(info_book)
    
def add_page(info_page):
    data_mngr.record_page(info_page)

def add_page_table(info_page_table):
    data_mngr.record_page_table(info_page_table)
    
def add_metadata(info_metadata):
    data_mngr.record_metadata(info_metadata)
    
def add_cell(info_cell):
    data_mngr.record_cell(info_cell)

def add_workflow_transaction(info_workflow_transaction):
    data_mngr.record_workflow_transaction(info_workflow_transaction)
    
def get_book(book_id):
    return data_mngr.get_book(book_id)

def get_page(book_id, num_page):
    return data_mngr.get_page(book_id, num_page)

def get_page_table(book_id, page_id):
    return data_mngr.get_page_table(book_id, page_id)

def get_metadata(book_id, page_id, page_table_id):
    return data_mngr.get_metadata(book_id, page_id, page_table_id)

def get_cell(book_id, page_id, page_table_id):
    return data_mngr.get_cell(book_id, page_id, page_table_id)

def get_workflow_transaction(workflow_transaction_info):
    return data_mngr.get_workflow_transaction(workflow_transaction_info)

def delete_workflow_transaction(workflow_transaction_info):
    return data_mngr.delete_workflow_transaction(workflow_transaction_info)

# App functions
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

def create_and_close_t1(app, short_name):
    o = app.get("/api/%s/init_and_close_t1" % short_name)
    return o

def done_task(app, task_id):
    o = app.get("/api/" + str(task_id) + "/done")
    return o

def get_book_data(book_id):
    return get_archive_book_data(book_id)

def authenticate_fb_user(base_url):
    auth = dict(facebook_user_id="12345", email="email@teste", name="fb-teste", full_name="fb-teste-fullname")
    r = requests.post(base_url + "/api/user/authenticate_facebook_user", data=json.dumps(auth), headers={'dataType': 'json', 'content-type': 'application/json'})
    print("Authenticate a FB User: " + json.loads(r.text)['response'])
    return auth

def submit_answer(base_url, task_run):
    requests.post(base_url + "/api/taskrun", data=json.dumps(task_run), headers={'dataType': 'json', 'content-type': 'application/json'})
    