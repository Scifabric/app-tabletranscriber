import requests
import json

from app_tt.core import app as flask_app


def archiveBookData(bookid):
    """
    Get internet archive book infos

    :arg book_id: Internet archive book id
    :returns: A dict with metadata from internet archive
    :rtype: dict

    """
    query = "http://archive.org/metadata/" + bookid
    data = json.loads(requests.get(query).content)
    img = "http://www.archive.org/download/" + bookid + "/page/n7_w100_h100"
    default_dict = {"title": None, "publisher": None,
                    "volume": None, "contributor": None}
    known_dict = dict(img=img, bookid=bookid)

    for key in default_dict:
        try:
            default_dict[key] = data["metadata"][key]
        except:
            print "This book does not have %s key" % key
            
    if default_dict['volume'] != None:
        default_dict['title'] = default_dict['title'] + ' (Vol. ' + default_dict['volume'] + ')'

    return dict(known_dict.items() + default_dict.items())

def setUrl_(arch, short_name, server=flask_app.config['URL_TEMPLATES']):
    text = ""
    for line in arch.readlines():
        line = line.replace("#server", server)
        line = line.replace("#task_shortname#", short_name.encode('utf-8'))
        text += line

    return text