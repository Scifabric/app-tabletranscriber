import urllib
import urllib2
import json
import string
from optparse import OptionParser
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta

def url_template_edit(server,file):
    text = ""
    for line in open(file).readlines():
        line = line.replace("#server",server)
        text += line
    
    return text


def get_tt_images(bookId):
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
    for idx in range(int(imagecount)-2):
        print 'Retrieved img: %s' % idx
        imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx,WIDTH,HEIGHT)
        imgUrl_b = imgUrls + str(idx)
        imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b})
    
    return imgList


if __name__ == "__main__":
    imgs = get_tt_images("estatisticasdodi1950depa")
    select = Apptt_select("tt-select")

    for img in imgs:
        select.add_task(img)
