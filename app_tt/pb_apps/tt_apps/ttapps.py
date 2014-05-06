# -*- coding: utf-8 -*-
from app_tt.core import app as flask_app
import app_tt.pb_apps.apps as app
import urllib2
import os
import app_tt.meb_util as meb_util
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception
from app_tt.core import logger

class Apptt_select(app.Apptt):
    """
       Selection app class
    """
    
    def __init__(self, **keyargs):
        if "short_name" in keyargs.keys():
            if "_tt1" in keyargs['short_name']:
                short_name = keyargs['short_name']
            else:
                logger.error(Meb_ttapps_exception(5, -1, "-"))
                raise Meb_ttapps_exception(5, -1, "-")
        else:
            logger.error(Meb_ttapps_exception(1, -1, "-"))
            raise Meb_ttapps_exception(1, -1, "-")
        
        if "title" in keyargs.keys():
            title = keyargs['title'] + " "
        else:
            title = ""
        
        app_name = title + unicode("Seleção", "utf-8")

        super(Apptt_select, self).__init__(
            app_name,
            short_name,
            "Por favor. Selecione as páginas com tabela.")

        super(Apptt_select, self).set_template(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/template-select.html")), short_name))

        super(Apptt_select, self).set_long_description(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/long_description-select.html")), short_name))
        
        super(Apptt_select, self).add_app_infos(
            dict(thumbnail=flask_app.config['URL_TEMPLATES']
                 + "/images" 
                 + "/long_description_selection.png"))
        
        logger.info("Create task type 1")


class Apptt_meta(app.Apptt):
    """
       Meta app class
    """
    
    def __init__(self, **keyargs):
        if "short_name" in keyargs.keys():
            if "_tt2" in keyargs['short_name']:
                short_name = keyargs['short_name']
            else:
                logger.error(Meb_ttapps_exception(6, -1, "-"))
                raise Meb_ttapps_exception(6, -1, "-")
        else:
            raise Meb_ttapps_exception(2, -1, "-")
        
        if "title" in keyargs.keys():
            title = keyargs['title'] + " "
        else:
            title = ""
        
        app_name = title + unicode("Marcação", "utf-8")

        super(Apptt_meta, self).__init__(
            app_name, short_name,
            "Marque e descreva as tabelas ou corrija as marcações.")

        super(Apptt_meta, self).set_template(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/template-meta.html")), short_name))

        super(Apptt_meta, self).set_long_description(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/long_description-meta.html")), short_name))
        
        super(Apptt_meta, self).add_app_infos(
            dict(
                sched="incremental",
                thumbnail=flask_app.config['URL_TEMPLATES']
                + "/images"
                + "/long_description_meta.png"))
        
        logger.info("Create task type 2")


class Apptt_struct(app.Apptt):
    """
       Struct app class
    """
    
    def __init__(self, **keyargs):

        if "short_name" in keyargs.keys():
            if "_tt3" in keyargs['short_name']:
                short_name = keyargs['short_name']
            else:
                logger.error(Meb_ttapps_exception(7, -1, "-"))
                raise Meb_ttapps_exception(7, -1, "-")
        else:
            raise Meb_ttapps_exception(3, -1, "-")

        if "title" in keyargs.keys():
            title = keyargs['title'] + " "
        else:
            title = ""

        app_name = title + unicode("Estrutura", "utf-8")
        
        super(Apptt_struct, self).__init__(
            app_name, short_name,
            "Por favor. Corrija as linhas e colunas da tabela.")

        super(Apptt_struct, self).set_template(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates/template-struct.html")),
            short_name))

        super(Apptt_struct, self).set_long_description(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/long_description-struct.html")), short_name))

        try:
            self.__create_dirs(flask_app.config['CV_MODULES'], short_name[:-4])
            logger.info("TT folders created")
        except OSError, e:
            logger.error(e)
        
        super(Apptt_struct, self).add_app_infos(
            dict(
                sched="incremental",
                thumbnail=flask_app.config['URL_TEMPLATES']
                + "/images"
                + "/long_description_struct.png"))
        
        logger.info("Create task type 3")

    def __create_dirs(self, path, short_name):
        """
          Create dirs to store book's images to cv-modules
        """
        
        dirs = ["alta_resolucao",
                "baixa_resolucao",
                "metadados/entrada",
                "metadados/saida",
                "metadados/tabelasAlta",
                "metadados/tabelasBaixa",
                "metadados/respostaUsuarioTT",
                "metadados/modelPreview",
                "transcricoes",
                "transcricoes/texts",
                "transcricoes/confidences",
                "selections"]

        for d in dirs:
            p = "%s/books/%s/%s" % (path, short_name, d)
            if not os.path.exists(p):
                os.makedirs(p)


class Apptt_transcribe(app.Apptt):
    """
       Transcribe app class
    """
    
    def __init__(self, **keyargs):

        if "short_name" in keyargs.keys():
            if "_tt4" in keyargs['short_name']:
                short_name = keyargs['short_name']
            else:
                logger.error(Meb_ttapps_exception(8, -1, "-"))
                raise Meb_ttapps_exception(8, -1, "-")
        else:
            raise Meb_ttapps_exception(4, -1, "-")

        if "title" in keyargs.keys():
            title = keyargs['title'] + " "
        else:
            title = ""
        
        app_name = title + unicode("Transcrição", "utf-8")
    
        super(Apptt_transcribe, self).__init__(
            app_name, short_name,
            "Por favor. Corrija o conteúdo das células da tabela.")

        super(Apptt_transcribe, self).set_template(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates/template-transcribe.html")),
            short_name))

        super(Apptt_transcribe, self).set_long_description(meb_util.set_url(
            urllib2.urlopen(
                urllib2.Request(
                    flask_app.config['URL_TEMPLATES']
                    + "/templates"
                    + "/long_description-transcribe.html")), short_name))
        
        super(Apptt_transcribe, self).add_app_infos(
            dict(
                 sched="incremental",
                 thumbnail=flask_app.config['URL_TEMPLATES']
                 + "/images"
                 + "/long_description_transcribe.png"))
        
        logger.info("Create task type 4")


