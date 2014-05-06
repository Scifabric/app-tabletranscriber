# -*- coding: utf-8 -*-

import requests
import json
import urllib2

from app_tt.core import app as flask_app, logger
from app_tt.meb_exceptions.meb_exception import Archive_book_data_exception

def get_archive_book_data(bookid):
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
            logger.error(Archive_book_data_exception(1, key))
            raise Archive_book_data_exception(1, key)
            
    if default_dict['volume'] != None:
        default_dict['title'] = default_dict['title'] + ' (Vol. ' + default_dict['volume'] + ')'

    return dict(known_dict.items() + default_dict.items())


def get_tt_images(bookId):
    """
    Get public book images from internet archive server

    :returns: A list with dicts containing images urls and index.
    :rtype: list

    """
    
    WIDTH = 550
    HEIGHT = 700

    logger.info('Contacting archive.org')

    url = "http://archive.org/metadata/"
    query = url + bookId
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    output = json.loads(data)
    imgList = []

    if output:
        n_pages = None
        try:
            if output['metadata'].has_key('imagecount'):
                n_pages = output['metadata']['imagecount']
            elif output['metadata'].has_key('numero_de_paginas_do_item'):
                n_pages = output['metadata']['numero_de_paginas_do_item']
        except KeyError:
            logger.error(Archive_book_data_exception(1, "imagecount or numero_de_paginas_do_item"))
            raise Archive_book_data_exception(1, "imagecount or numero_de_paginas_do_item")
            
        imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"
        for idx in range(int(n_pages)):
            logger.info('Retrieved img: %s' % idx)
            page = idx
            imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx, WIDTH, HEIGHT)
            imgUrl_b = imgUrls + str(idx)
            imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b,
                            'page': page})

    return imgList


def set_url(arch, short_name, server=flask_app.config['URL_TEMPLATES']):
    text = ""
    for line in arch.readlines():
        line = line.replace("#server", server)
        line = line.replace("#app_shortname#", short_name.encode('utf-8'))
        text += line

    return text