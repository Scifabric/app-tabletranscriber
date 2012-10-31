#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import urllib2
import json
import re
import string
from optparse import OptionParser
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
        imgList.append({'link':  imgUrl_m})
    
    return imgList



if __name__ == "__main__":
    imgs = get_tt_images("estatisticasdodi1950depa")
    meta = Apptt_meta("tt-meta")
    for img in imgs:
        meta.add_task(img)
