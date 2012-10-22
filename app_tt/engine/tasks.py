import os
import sys
from celery import Celery
import urllib2
import json

# sys.path.append(os.path.abspath("..")+"/pb_apps/tt_apps/")
# from ttapps import Apptt_select
# from ttapps import Apptt_meta


celery = Celery('tasks', backend='amqp', broker='amqp://celery:celery@localhost:5672/celery')


@celery.task
def check_task(task_id):
    return task_id

# def create_apps(book_id):
#     tt_select = Apptt_select(book_id + "_tt1")
#     tt_meta = Apptt_meta(book_id + "_tt2")
    
#     imgs = __get_tt_images(book_id)

#     if(imgs.len > 0):
#         for image in imgs:
#             tt_select.add_task(image)
#         return True
#     else:
#         raise ValueError("Error didn't find book id") 

#     return False


# def __get_tt_images(bookId):
#     """
#     Gets public book images from internet archive server
#     :returns: A list of book images.
#     :rtype: list
#     """
#     WIDTH = 550
#     HEIGHT = 700
    
#     print('Contacting archive.org')
   
#     url = "http://archive.org/metadata/"
#     query = url + bookId
#     urlobj = urllib2.urlopen(query)
#     data = urlobj.read()
#     urlobj.close()
#     output = json.loads(data)
    
#     imagecount = output['metadata']['imagecount']
#     imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"

#     imgList = []
#     for idx in range(int(imagecount)-2):
#         print 'Retrieved img: %s' % idx
#         imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx,WIDTH,HEIGHT)
#         imgUrl_b = imgUrls + str(idx)
#         imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b})
    
#     return imgList
