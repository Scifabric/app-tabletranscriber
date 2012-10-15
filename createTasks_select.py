import urllib
import urllib2
import json
import string
from optparse import OptionParser
from PybossaApp import App

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
    # Arguments for the application
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", dest="api_url",
                      help="PyBossa URL http://domain.com/", metavar="URL")
    parser.add_option("-k", "--api-key", dest="api_key",
                      help="PyBossa User API-KEY to interact with PyBossa",
                      metavar="API-KEY")
    parser.add_option("-c", "--create-app", action="store_true",
                      dest="create_app",
                      help="Create the application",
                      metavar="CREATE-APP")
    parser.add_option("-t", "--update-template", action="store_true",
                      dest="update_template",
                      help="Update Tasks template",
                      metavar="UPDATE-TEMPLATE"
                     )
    parser.add_option("-n", "--number-answers",
                      dest="n_answers",
                      help="Number of answers per task",
                      metavar="N-ANSWERS"
                     )
    parser.add_option("-s", 
                      "--server", 
                      dest="server", 
                      help="Table Transcriber Select Server URL", 
                      metavar="TT-URL")
    
    parser.add_option("-b", 
                      "--book", 
                      dest="book", 
                      help="Table Transcriber Select Book Name", 
                      metavar="BOOK-NAME")
    
    parser.add_option("-r", "--recursive", action="store_true", dest="recursive")


    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()


    if (options.verbose):
        print('Running against PyBosssa instance at: %s' % options.api_url)
        print('Using API-KEY: %s' % options.api_key)

    if not options.book:
            parser.error("You must choice --book, or a --recursive option")

    else:
        images = get_tt_images(options.book)
    
    app = App("Name", "testeapp", "Description", "3d39044f-bc93-4226-b44c-6e88f3fa76c8",  "http://localhost:5000")

    for image in images:
        app.add_task(image)

    if options.update_template:
        print "Updating app template"
        app.set_template(url_template_edit(options.server,"template-select.html"))
