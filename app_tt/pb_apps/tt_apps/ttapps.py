# -*- coding: utf-8 -*-
import app_tt.default_settings as settings
import app_tt.pb_apps.apps as app
import urllib2
import os
import pbclient
from optparse import OptionParser

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


class Apptt_struct(app.Apptt):
    def __init__(self, short_name):
        super(Apptt_struct, self).__init__("Estrutura das tabelas", short_name,
                        "Por favor. Corrija as linhas e colunas da tabela.",
                        settings.API_KEY, settings.PYBOSSA_URL)

        self.__create_dirs(short_name[:-4], settings.BOOKS_DIR )

    def __create_dirs(self, short_name, path):
        dirs = ["alta_resolucao", "baixa_resolucao",
                "metadados/entrada", "metadados/saida",
                "metadados/tabelasAlta", "metadados/tabelasBaixa",
                "transcricoes"]

        for d in dirs:
            os.makedirs("%s/%s/%s" % (path, short_name, d))


def __setUrl__(arch, short_name, server=settings.URL_TEMPLATES):
    text = ""
    for line in arch.readlines():
        line = line.replace("#server", server)
        line = line.replace("#task_shortname#", short_name.encode('utf-8'))
        text += line

    return text


if __name__ == "__main__":
    pbclient.set('endpoint', settings.PYBOSSA_URL)
    pbclient.set('api_key', settings.API_KEY)
    
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--update-template",
                dest="app_short_name", help="Update app template",
                metavar="SHORT_NAME")

    (options, args) = parser.parse_args()

    if options.app_short_name:
        app_short_name = options.app_short_name
        print app_short_name
        app = pbclient.find_app(short_name=app_short_name)[0]
        app_type = app_short_name[-4:]
        template_type = None
        
        if app_type == "_tt1":
            template_type = "template-select.html"
        elif app_type == "_tt2":
            template_type = "template-meta.html"

        if template_type:
            new_template = __setUrl__(
                    urllib2.urlopen(
                        urllib2.Request(
                            settings.URL_TEMPLATES + os.sep + "templates" + os.sep + template_type)), app_short_name)

            app.info['task_presenter'] = new_template
    
            pbclient.update_app(app)
