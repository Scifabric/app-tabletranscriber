# -*- coding: utf-8 -*-


class Meb_exception( Exception ):
    exception_msgs = {}
    
    def __init__(self, exc_code):
        try:
            if self.exception_msgs.has_key(exc_code):
                self.code = exc_code
                self.msg = self.exception_msgs[self.code]
            else:
                raise
        except Exception:
            print "Invalid MEB Exception code"
    
    def __str__(self):
        return repr(unicode(self.exception_msgs[self.code], "utf-8"))
    
    def set_exception_msgs(self, msgs):
        self.exception_msgs = msgs

class Meb_apps_exception( Meb_exception ):
    exception_msgs = {
           1 : "MEB-APPS-1: App with empty name",
           2 : "MEB-APPS-2: App with empty shortname",
           3 : "MEB-APPS-3: App with empty description",
           4 : "MEB-APPS-4: Error creating the application",
           5 : "MEB-APPS-5: Error you must supply values into info dict"
          }

    def __init__(self, exc_code):
        self.set_exception_msgs(self.exception_msgs)
        super(Meb_apps_exception, self).__init__(exc_code)

