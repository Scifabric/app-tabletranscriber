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


def delete_app(api_url, api_key, id):
    """
    Deletes the Table Transcriber Meta application.

    :arg integer id: The ID of the application
    :returns: True if the application has been deleted
    :rtype: boolean
    """
    request = urllib2.Request(api_url + '/api/app/' + str(id) + \
                              '?api_key=' + api_key)
    request.get_method = lambda: 'DELETE'

    if (urllib2.urlopen(request).getcode() == 204):
        return True
    else:
        return False


def update_app(api_url, api_key, id, name=None):
    """
    Updates the name of the Table Transcriber Meta application
    :arg integer id: The ID of the application
    :arg string name: The new name for the application
    :returns: True if the application has been updated
    :rtype: boolean
    """
    data = dict(id=id, name=name)
    data = json.dumps(data)
    request = urllib2.Request(api_url + '/api/app/' + str(id) + \
                              '?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')
    request.get_method = lambda: 'PUT'

    if (urllib2.urlopen(request).getcode() == 200):
        return True
    else:
        return False


def create_app(api_url, api_key, server, name=None, short_name=None,
               description=None):
    """
    Creates the Table Transcriber Meta application.
    :arg string server: The application url.
    :arg string name: The application name.
    :arg string short_name: The slug application name.
    :arg string description: A short description of the application.

    :returns: Application ID or 0 in case of error.
    :rtype: integer
    """
    if(server.endswith('/')):
        server = server[:server.rfind('/')]
    print('Creating app')
    name = u'Table Transcriber Meta'  # Name with a typo
    short_name = u'tt-meta'
    description = u'Por favor, marque e descreva as tabelas.'
    # JSON Blob to present the tasks for this app to the users
    # First we read the template:
    file = open('template-meta.html')
    text = url_template_edit(server,file)
    file.close()
    # HTML Blob with a long description for the application
    file = open('long_description-meta.html')
    long_description = url_template_edit(server, file)
    file.close()
    
    info = dict(thumbnail=server + "/images/imagettPresenter.png",
                 task_presenter=text)
    data = dict(name=name, short_name=short_name, description=description,
                long_description=long_description,
                hidden=0, info=info)
    data = json.dumps(data)

    # Checking which apps have been already registered in the DB
    apps = json.loads(urllib2.urlopen(api_url + '/api/app' + \
                      '?api_key=' + api_key).read())
    for app in apps:
        if app['short_name'] == short_name:
            print('{app_name} app is already registered in the DB'\
                    .format(app_name=name))
            print('Deleting it!')
            if (delete_app(api_url, api_key, app['id'])):
                print "Application deleted!"
    print("The application is not registered in PyBOSSA. Creating it...")
    # Setting the POST action
    request = urllib2.Request(api_url + '/api/app?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')

    # Create the app in PyBOSSA
    output = json.loads(urllib2.urlopen(request).read())
    if (output['id'] != None):
        print("Done!")
        print("Ooooops! the name of the application has a typo!")
        print("Updating it!")
        if (update_app(api_url, api_key, output['id'],
            "Table Transcriber Meta")):
            print "Application name fixed!"
            return output['id']
        else:
            print "An error has occurred"
    else:
        print("Error creating the application")
        return 0


def create_task(api_url, api_key, app_id, n_answers, image):
    """
    Creates tasks for the application

    :arg integer app_id: Application ID in PyBossa.
    :returns: Task ID in PyBossa.
    :rtype: integer
    """
    # Data for the tasks
    info = dict(n_answers=int(n_answers), link=image['link'])

    data = dict(app_id=app_id, state=0, info=info,
                 calibration=0, priority_0=0)

    data = json.dumps(data)

    # Setting the POST action
    request = urllib2.Request(api_url + '/api/task' + '?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')

    # Create the task
    output = json.loads(urllib2.urlopen(request).read())
    if (output['id'] != None):
        return True
    else:
        return False

def url_template_edit(server,file):
    text = ""
    for line in file.readlines():
        line = line.replace("#server",server)
        text += line
    
    return text

def update_template(api_url, api_key, server, app='tt-meta'):
    """
    Update tasks template and long description for the application tt-meta

    :arg string app: Application short_name in PyBossa.
    :arg string server: The application url.
    :returns: True when the template has been updated.
    :rtype: boolean
    """
    request = urllib2.Request('%s/api/app?short_name=%s' %
                              (api_url, app))
    request.add_header('Content-type', 'application/json')

    res = urllib2.urlopen(request).read()
    res = json.loads(res)
    res = res[0]
    if res.get('short_name'):
        # Re-read the template
        file = open('template-meta.html')
        text = url_template_edit(server,file)
        file.close()
        # Re-read the long_description
        file = open('long_description-meta.html')
        long_desc = url_template_edit(server, file)
        file.close()
        info = dict(thumbnail=res['info']['thumbnail'], task_presenter=text)
        data = dict(id=res['id'], name=res['name'],
                    short_name=res['short_name'],
                    description=res['description'], hidden=res['hidden'],
                    long_description=long_desc,
                    info=info)
        data = json.dumps(data)
        request = urllib2.Request(api_url + '/api/app/' + str(res['id']) + \
                                  '?api_key=' + api_key)
        request.add_data(data)
        request.add_header('Content-type', 'application/json')
        request.get_method = lambda: 'PUT'

        if (urllib2.urlopen(request).getcode() == 200):
            return True
        else:
            return False

    else:
        return False

    # Data for the tasks
    info = dict(n_answers=2, link=photo['link'], url_m=photo['url_m'],
                 url_b=photo['url_b'])
    data = dict(app_id=app_id, state=0, info=info,
                calibration=0, priority_0=0)
    data = json.dumps(data)

    # Setting the POST action
    request = urllib2.Request(api_url + '/api/task' + '?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')

    # Create the task
    output = json.loads(urllib2.urlopen(request).read())
    if (output['id'] != None):
        return True
    else:
        return False


def get_recursive_tt_images(url):
    """
    Gets recursively public books images from a given server
    :returns: A list of book images photos.
    :rtype: list
    """
    # Get the ID of the images and load it in the output var
    if(url.endswith('/')):
        url = url[:url.rfind('/')]
    url = url + "/books/"
    patternLinks = re.compile(r'<a\s.*?href\s*?=\s*?"(.*?)"', re.DOTALL | re.IGNORECASE)
    
    try:
        urlobj = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print("Error: " + url + "Doesn't exist")
        exit()
    
    print('Contacting ' + url + ' for images')
   
    data = urlobj.read()
    urlobj.close()
    iterator = patternLinks.finditer(data);
    
    imageList = []
    
    # process individual items
    for match in iterator:
        fileUrl = match.group(1)
        dirUrl = url[:url.rfind('/')] + '/' + fileUrl
        if(url[:url.rfind('/')] == dirUrl[:dirUrl.rfind('//')] ):
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
                else: # relative url
                    imageUrl = dirUrl[:dirUrl.rfind('/')] + '/' + dirfileUrl
            
                imageList.append({'link' : imageUrl})
    
    if(len(imageList) == 0):
        print("Error: Couldn't find any image")
        exit()
    
    return imageList

def get_tt_images(url,book):
    """
    Gets public book images from a given server
    :returns: A list of book images photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    patternLinks = re.compile(r'<a\s.*?href\s*?=\s*?"(.*?)"', re.DOTALL | re.IGNORECASE)
    
    if(url.endswith('/')):
        url = url[:url.rfind('/')]
    
    url = url + "/books/" + book
    try:
        urlobj = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print("Error: " + url + "Doesn't exist")
        exit()
    
    print('Contacting ' + url + ' for images')
    urlobj = urllib2.urlopen(url)
    data = urlobj.read()
    urlobj.close()
    iterator = patternLinks.finditer(data);
    
    imageList = []
    
    # process individual items
    for match in iterator:
        fileUrl = match.group(1)
        
        if fileUrl.endswith(".png") or fileUrl.endswith(".jpg"):
            urlType = re.match('^https?://(.*)', fileUrl)
            # absolute URL
            if urlType:
                filename = urlType.group(1)
                imageUrl = urlType.group(0)
            else: # relative url
                imageUrl = url + '/' + fileUrl
            
            imageList.append({'link' : imageUrl})
    
    if(len(imageList) == 0):
        print("Error: Couldn't find any image")
        exit()
    
    return imageList


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
                      help="Table Transcriber Server URL", 
                      metavar="TT-URL")
    
    parser.add_option("-b", 
                      "--book", 
                      dest="book", 
                      help="Table Transcriber Book Name", 
                      metavar="BOOK-NAME")
    
    parser.add_option("-r", "--recursive", action="store_true", dest="recursive")


    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()

    if not options.api_url:
        options.api_url = 'http://localhost:5000/'

    if not options.api_key:
        parser.error("You must supply an API-KEY to create an \
                      applicationa and tasks in PyBossa")
    if not options.server:
        parser.error("You must choose a Table Transcriber's server URL ex: http://localhost/TTappname")

    if (options.verbose):
        print('Running against PyBosssa instance at: %s' % options.api_url)
        print('Using API-KEY: %s' % options.api_key)

    if options.create_app:
        if not options.recursive:
            if not options.book:
                parser.error("You must choice --book, or a --recursive option")

        if options.book:
            print "aqui"
            images = get_tt_images(options.server,options.book)
        else:
            images = get_recursive_tt_images(options.server)
        
        app_id = create_app(options.api_url, options.api_key, options.server)
        # First of all we get the URL photos
        
        # Finally, we have to create a set of tasks for the application
        # For this, we get first the image URLs
        for image in images:
            if options.n_answers:
                create_task(options.api_url, options.api_key, app_id,
                            options.n_answers, image)
            else:
                create_task(options.api_url, options.api_key, app_id,
                            30, image)

    if options.update_template:
        print "Updating app template"
        update_template(options.api_url, options.api_key, options.server)

    if not options.create_app and not options.update_template:
        parser.error("Please check --help or -h for the available options")
