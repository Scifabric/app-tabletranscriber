from celery import Celery
import urllib2
import json
from celery import task
import app_tt.default_settings as settings
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta

BROKER_URL = "amqp://celery:celery@localhost:5672/celery"

celery = Celery('tasks', backend='amqp', broker=BROKER_URL)
#celery.config_from_object('app_tt.engine.celeryconfig')

@task(name="app_tt.engine.tasks.check_task")
def check_task(task_id):
    task = json.loads(urllib2.urlopen("%s/api/task/%s?api_key=%s" % (settings.PYBOSSA_URL, task_id, settings.API_KEY)).read())

    if(task):
        if(task["state"] == 'completed'):
            return True
        else:
            return False
    else:
        raise ValueError("Task not found")


@task(name="app_tt.engine.tasks.create_apps")
def create_apps(book_id):
    imgs = __get_tt_images(book_id)

    if(len(imgs) > 0):
        tt_select = Apptt_select(book_id + "_tt1")
        tt_meta = Apptt_meta(book_id + "_tt2")

        for image in imgs:
            tt_select.add_task(image)
        return True
    else:
        raise ValueError("Error didn't find book id")

    return False


def __get_tt_images(bookId):
    """
    Gets public book images from internet archive server
    :returns: A list of book images.
    :rtype: list
    """
    WIDTH = 550
    HEIGHT = 700

    print('Contacting archive.org')

    url = "http://archive.org/metadata/"
    query = url + bookId
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    output = json.loads(data)

    imagecount = output['metadata']['imagecount']
    imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"

    imgList = []
    for idx in range(int(imagecount) - 2):
        print 'Retrieved img: %s' % idx
        imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx, WIDTH, HEIGHT)
        imgUrl_b = imgUrls + str(idx)
        imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b})

    return imgList
