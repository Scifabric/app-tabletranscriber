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
        """
          Create a new app with name, shortname and description passed in constructor
          and with category_id = 1 and return app.id. Or return the app.id from the app registered
          in pybossa database.
          
          :returns: app.id
          :rtype: int
          
        """
        
        apps = pbclient.find_app(short_name=self.short_name)
        if not len(apps) == 0:
            app = apps[0]
            msg = '{app_name} app is already registered in the DB'.format(app_name=app.name.encode('utf-8', 'replace'))
            logger.info(unicode(msg, "utf-8"))
            return app.id
        else:
            logger.info("The application is not registered in PyBOSSA. Creating it...")
            ans = pbclient.create_app(name=self.name, short_name=self.short_name, description=self.description)
            if ans:
                app = pbclient.find_app(short_name=self.short_name)[0]
                app.info = dict(newtask="%s/app/%s/newtask" % (flask_app.config['PYBOSSA_URL'], self.short_name))
                app.category_id = 1
                pbclient.update_app(app)
                return app.id
            else:
                logger.error(Meb_apps_exception(4))
                raise Meb_apps_exception(4)
        
    def set_name(self, name):
        """
          Set app name
          
          :arg string name: name of the app
        """
        
        app = pbclient.get_app(self.app_id)
        app.name = name
        pbclient.update_app(app)

    def set_template(self, template_text):
        """
          Set app's template
          
          :arg string template_text: content of template in string format
          
        """
        
        app = pbclient.get_app(self.app_id)
        app.info['task_presenter'] = template_text
        pbclient.update_app(app)

    def set_long_description(self, long_description_text):
        """
          Set app's long description template
          
          :arg string long_description_text: content of long description template
                                      in string format
        """
        
        app = pbclient.get_app(self.app_id)
        app.long_description = long_description_text
        pbclient.update_app(app)

    def add_app_infos(self, info_values):
        """
           Add new info values to info attribute from this app
           
           :arg dict info_values: dict with infos and respectives values to add
                             to the app
           
        """
        
        app = pbclient.get_app(self.app_id)

        if(type(info_values) is dict):
            for info_key in info_values.keys():
                app.info[str(info_key)] = info_values[info_key]
        else:
            logger.error(Meb_apps_exception(5))
            raise Meb_apps_exception(5)

        pbclient.update_app(app)

    def get_tasks(self):
        """
           Return tasks from this app
           
           :return list of tasks
           :rtype list
           
        """
        
        return pbclient.get_tasks(self.app_id, sys.maxint)

    def add_task(self, task_info, priority=0):
        """
          Add task to this app
          
          :arg dict task_info: dict with info to task
          :arg float priority: priority of task (must be between 0 and 1), default = 0
          
        """
        
        if priority < 0 or priority > 1:
            raise Meb_apps_exception(6)
        
        pbclient.create_task(self.app_id, task_info, priority_0=priority)
