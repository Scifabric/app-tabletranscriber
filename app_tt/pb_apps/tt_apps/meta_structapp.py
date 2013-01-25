# -*- coding: utf-8 -*-
import app_tt.default_settings as settings
import app_tt.pb_apps.apps as app
import os
import urllib2
import re


class Apptt_meta_struct(app.Apptt):
    def __init__(self, short_name):
        super(Apptt_meta_struct, self).__init__(
                "Enxergue a melhor tabela",
                short_name, "Qual das tabelas está melhor construida?",
                settings.API_KEY, settings.PYBOSSA_URL)
        super(Apptt_meta_struct, self).set_template(
                 __setUrl__(
                      os.path.dirname(__file__) + os.sep + "templates" +
                      os.sep + "template-meta-struct.html"))

        super(Apptt_meta_struct, self).set_long_description(
                __setUrl__(
                     os.path.dirname(__file__) + os.sep + "templates" +
                     os.sep + "long_description-meta-struct.html"))


def __setUrl__(arch, server=settings.URL_TEMPLATES):
    text = ""
    for line in open(arch).readlines():
        line = line.replace("#server", server)
        text += line

    return text


def get_images_url(url):
    """
    Gets recursively public books images from a given server
    :returns: A list of book images photos.
    :rtype: list
    """
    # Get the ID of the images and load it in the output var
    patternLinks = re.compile(r'<a\s.*?href\s*?=\s*?"(.*?)"',
            re.DOTALL | re.IGNORECASE)

    try:
        urlobj = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print("Error: " + url + "Doesn't exist")
        exit()

    print('Contacting ' + url + ' for images')

    data = urlobj.read()
    urlobj.close()
    iterator = patternLinks.finditer(data);
    dataDir = {}

    # process individual items
    for match in iterator:
        fileUrl = match.group(1)
        dirUrl = url[:url.rfind('/')] + '/' + fileUrl
        if(url[:url.rfind('/')] == dirUrl[:dirUrl.rfind('//')]):
            continue
        dirobj = urllib2.urlopen(url[:url.rfind('/')] + '/' + fileUrl)
        dirdata = dirobj.read()
        dirobj.close()
        diriterator = patternLinks.finditer(dirdata)
        for dirmatch in diriterator:
            dirfileUrl = dirmatch.group(1)
            if dirfileUrl.endswith(".png") or fileUrl.endswith(".jpg"):
                urlType = re.match('^https?://(.*)', fileUrl)
            # absolute URL
                if urlType:
                    filename = urlType.group(1)
                    imageUrl = urlType.group(0)
                else:  # relative url
                    imageUrl = dirUrl[:dirUrl.rfind('/')] + '/' + dirfileUrl

                parse_dir_name = dirUrl[:dirUrl.rfind('/')]
                parse_dir_name = parse_dir_name[parse_dir_name.rfind('/') + 1:]
                if(parse_dir_name not in dataDir.keys()):
                    dataDir[parse_dir_name] = []
                dataDir[parse_dir_name].append(imageUrl)

    if(len(dataDir.keys()) == 0):
        print("Error: Couldn't find any image")
        exit()

    return dataDir


if __name__ == '__main__':

    app = Apptt_meta_struct("random-tt-meta-struct")
    
    app.add_app_infos(dict(sched="random", tutorial=
                __setUrl__(
                     os.path.dirname(__file__) + os.sep + "templates" +
                     os.sep + "tutorial-meta-struct.html")))

    imgDict = get_images_url("http://bacalhau.lsd.ufcg.edu.br/transcriber/2packages/")

    for dic in imgDict.keys():          #Creates tasks combining 2-2
         images = imgDict[dic]
         for cur_img in range(len(images)):
             for next_img in range(cur_img+1, len(images)):
                 app.add_task(dict(package=dic, imgs_url=[images[cur_img],
                                   images[next_img]], n_answers=2), 2)
