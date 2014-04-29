# -*- coding: utf-8 -*-
from app_tt.core import app as flask_app, pbclient, logger
import json
import sys
import urllib2
from app_tt.meb_exceptions.meb_exception import Meb_apps_exception

class Apptt(object):
    def __init__(self, name, short_name, description):
        """
        Pybossa application constructor

        :arg string name: The application name.
        :arg string short_name: The slug application name.
        :arg string description: A short description of the application.
        """
        
        if name == "":
            logger.error(Meb_apps_exception(1))
            raise Meb_apps_exception(1)
        elif short_name == "":
            logger.error(Meb_apps_exception(2))
            raise Meb_apps_exception(2) 
        elif description == "":
            logger.error(Meb_apps_exception(3))
            raise Meb_apps_exception(3)
        
        self.short_name = short_name
        self.api_key = pbclient._opts['api_key']
        self.pybossa_url = pbclient._opts['endpoint']
        self.description = description
        self.name = name
        self.app_id = self.__create_app()
        
    def __create_app(self):

        info = dict(newtask="%s/app/%s/newtask" % (flask_app.config['PYBOSSA_URL'], self.short_name))
        data = dict(name=self.name, short_name=self.short_name,
                description=self.description, hidden=0,
                info=info, category_id=1)
        data = json.dumps(data)

        # Checking which apps have been already registered in the DB
        apps = pbclient.get_apps(sys.maxint)
        for app in apps:
            if app.short_name == self.short_name:
                logger.info('{app_name} app is already registered in the DB'
                         .format(app_name=app.name.encode('utf-8','replace')))
                
                return app.id
        
        logger.info("The application is not registered in PyBOSSA. Creating it...")
        
        logger.info("Request: " + self.pybossa_url + '/api/app?api_key=' +
                self.api_key)
        
        # Setting the POST action
        request = urllib2.Request(self.pybossa_url + '/api/app?api_key=' +
                self.api_key)
        request.add_data(data)
        request.add_header('Content-type', 'application/json')
        
        # Create the app in PyBOSSA
        output = json.loads(urllib2.urlopen(request).read())
        
        if (output['id'] is not None):
            return output['id']
        else:
            logger.error(Meb_apps_exception(4))
            raise Meb_apps_exception(4)

    def set_name(self, name):
        app = pbclient.get_app(self.app_id)
        app.name = name
        pbclient.update_app(app)

    def set_template(self, template_text):
        app = pbclient.get_app(self.app_id)
        app.info['task_presenter'] = template_text
        pbclient.update_app(app)

    def set_long_description(self, long_description_text):
        app = pbclient.get_app(self.app_id)
        app.long_description = long_description_text
        pbclient.update_app(app)

    def add_app_infos(self, info_values):
        app = pbclient.get_app(self.app_id)

        if(type(info_values) is dict):
            for info_key in info_values.keys():
                app.info[str(info_key)] = info_values[info_key]
        else:
            logger.error(Meb_apps_exception(5))
            raise Meb_apps_exception(5)

        pbclient.update_app(app)


    def get_tasks(self):
        return pbclient.get_tasks(self.app_id, sys.maxint)


    def add_task(self, task_info, priority=0):
        pbclient.create_task(self.app_id, task_info, priority_0=priority)
