# -*- coding: utf-8 -*-
import app_tt.default_settings as settings
import app_tt.pb_apps.apps as app
import urllib2
import os


class Apptt_select(app.Apptt):
    def __init__(self, short_name):
        super(Apptt_select, self).__init__("Seleção de tabelas", short_name,
                        "Por favor. Selecione as páginas com tabela.",
                        settings.API_KEY, settings.PYBOSSA_URL)
        
        super(Apptt_select, self).set_template(__setUrl__(
                urllib2.urlopen(
                    urllib2.Request(
                        settings.URL_TEMPLATES + os.sep + "templates" + os.sep + "template-select.html")), short_name))
       
        super(Apptt_select, self).set_long_description(__setUrl__(
           urllib2.urlopen(
               urllib2.Request(
                   settings.URL_TEMPLATES + os.sep + "templates" + os.sep + "long_description-select.html")), short_name))


class Apptt_meta(app.Apptt):
    def __init__(self, short_name):
        super(Apptt_meta, self).__init__("Marcação de tabelas", short_name,
                        "Por favor. Marque e descreva as tabelas.",
                        settings.API_KEY, settings.PYBOSSA_URL)
        
        super(Apptt_meta, self).set_template(__setUrl__(
                urllib2.urlopen(
                    urllib2.Request(
                        settings.URL_TEMPLATES + os.sep + "templates" + os.sep + "template-meta.html")), short_name ))
       
        super(Apptt_meta, self).set_long_description(__setUrl__(
            urllib2.urlopen(
                urllib2.Request(
                    settings.URL_TEMPLATES + os.sep + "templates" + os.sep + "long_description-meta.html")), short_name))


   
def __setUrl__(arch, short_name, server=settings.URL_TEMPLATES):
    text = ""
    for line in arch.readlines():
        line = line.replace("#server", server)
        line = line.replace("#task_shortname#", short_name.encode('utf-8'))
        text += line

    return text
