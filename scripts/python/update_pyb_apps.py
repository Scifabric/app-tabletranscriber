#!/usr/bin/python
# -*- coding: utf-8 -*-
from app_tt.meb_util import archiveBookData, setUrl_
from optparse import OptionParser
from app_tt.core import app as flask_app, pbclient
import urllib2


if __name__ == "__main__":
    usage = "usage: %prog [options]"
    
    parser = OptionParser(usage)
    
    parser.add_option(
        "-u", "--update-templates",
        dest="app_short_name", help="Update app templates: long-description and template",
        metavar="SHORT_NAME")
    
    (options, args) = parser.parse_args()
 
    if options.app_short_name:
        app_short_name = options.app_short_name
        print app_short_name
        apps = pbclient.find_app(short_name=app_short_name)
        
        if len(apps) == 0:
            print "App %s not found" % (app_short_name)
            exit(0)
        
        app = apps[0]
        app_type = app_short_name[-4:]
        template_type = None
        long_desc_type = None
        app_name = None
 
        if app_type == "_tt1":
            template_type = "template-select.html"
            long_desc_type = "long_description-select.html"
            app_name = unicode("Seleção", "utf-8")
        elif app_type == "_tt2":
            template_type = "template-meta.html"
            long_desc_type = "long_description-meta.html"
            app_name = unicode("Marcação", "utf-8")
        elif app_type == "_tt3":
            template_type = "template-struct.html"
            long_desc_type = "long_description-struct.html"
            app_name = unicode("Estrutura", "utf-8")
        elif app_type == "_tt4":
            template_type = "template-transcribe.html"
            long_desc_type = "long_description-transcribe.html"
            app_name = unicode("Transcrição", "utf-8")
 
        if template_type:
            new_template = setUrl_(
                urllib2.urlopen(
                    urllib2.Request(
                        flask_app.config['URL_TEMPLATES']
                        + "/templates/" + template_type)),
                app_short_name)
            
            new_long_desc_template = setUrl_(
                urllib2.urlopen(
                    urllib2.Request(
                        flask_app.config['URL_TEMPLATES'] + 
                                "/templates/" +
                                long_desc_type)), 
                     app_short_name)

            app.info['task_presenter'] = new_template
            app.long_description = new_long_desc_template
             
            book_id = app_short_name[:-4]
            bookInfo = archiveBookData(book_id)
            app.name = bookInfo['title'] + " " + app_name
            pbclient.update_app(app)