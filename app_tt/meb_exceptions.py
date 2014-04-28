
excepts = {
           1 : "MEB-1: App with empty name",
           2 : "MEB-2: App with empty shortname",
           3 : "MEB-3: App with empty description",
           4 : "MEB-4: Error creating the application",
           5 : "MEB-5: Error you must supply values into info dict"
          }


class meb_exception( Exception ):
    def __init__(self, exc_code):
        try:
            if excepts.has_key(exc_code):
                self.code = exc_code
                self.msg = excepts[self.code]
            else:
                raise
        except Exception:
            print "Invalid MEB Exception code"
    
    def __str__(self):
        return repr(unicode(excepts[self.code], "utf-8"))




