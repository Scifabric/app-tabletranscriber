# -*- coding: utf-8 -*-
from app_tt.core import pbclient
from optparse import OptionParser
from app_tt.meb_util import archiveBookData
from app_tt.meb_util import setUrl_
from app_tt.core import app as flask_app
import urllib2


if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option(
        "-u", "--update-template",
        dest="app_short_name", help="Update app template",
        metavar="SHORT_NAME")

    (options, args) = parser.parse_args()

    if options.app_short_name:
        app_short_name = options.app_short_name
        print app_short_name
        app = pbclient.find_app(short_name=app_short_name)[0]
        app_type = app_short_name[-4:]
        template_type = None
        app_name = None

        if app_type == "_tt1":
            template_type = "template-select.html"
            app_name = unicode("Seleção", "utf-8")
        elif app_type == "_tt2":
            template_type = "template-meta.html"
            app_name = unicode("Marcação", "utf-8")
        elif app_type == "_tt3":
            template_type = "template-struct.html"
            app_name = unicode("Estrutura", "utf-8")
        elif app_type == "_tt4":
            template_type = "template-transcribe.html"
            app_name = unicode("Transcrição", "utf-8")

        if template_type:
            new_template = setUrl_(
                urllib2.urlopen(
                    urllib2.Request(
                        flask_app.config['URL_TEMPLATES']
                        + "/templates/" + template_type)),
                app_short_name)

            app.info['task_presenter'] = new_template
            
            book_id = app_short_name[:-4]
            bookInfo = archiveBookData(book_id)
            app.name = bookInfo['title'] + " " + app_name
            pbclient.update_app(app)