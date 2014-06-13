
from app_tt.meb_exceptions.meb_exception import Meb_exception

class Meb_file_output_exception( Meb_exception ):
    def __init__(self, exc_code, task_id, bookId, imgId):
        msg = self.config_msg(exc_code, task_id, bookId, imgId)
        super(Meb_exception, self).__init__(exc_code, msg)

class Meb_file_output_exception_tt2( Meb_file_output_exception ):
    std_exception_msgs = {
                          1 : "MEB-FILE-OUTPUT-TT2-TASKS-1: Couldn't open output file"
                          }
    
    def __init__(self, exc_code, task_id, bookId, imgId):
        msg = self.config_msg(exc_code, task_id, bookId, imgId)
        super(Meb_file_output_exception_tt2, self).__init__(exc_code, msg)
    
    def config_msg(self, exc_code, taskid, bookId, imgId):
        return "%s | origin task id : %d | file url : books/%s/metadados/saida/image%d_model1.txt" % \
            (self.std_exception_msgs[exc_code], taskid, bookId, imgId)
            
            
class Meb_file_output_exception_tt3( Meb_file_output_exception ):
    std_exception_msgs = {
                          1 : "MEB-FILE-OUTPUT-TT3-TASKS-1: Couldn't open output file"
                          }
    
    def __init__(self, exc_code, task_id, bookId, imgId, tableId):
        msg = self.config_msg(exc_code, task_id, bookId, imgId, tableId)
        super(Meb_file_output_exception_tt3, self).__init__(exc_code, msg)
    
    def config_msg(self, exc_code, taskid, bookId, imgId, tableId):
        return "%s | origin task id : %d | file url : books/%s/metadados/respostaUsuarioTT/image%d_%d.txt" % \
            (self.std_exception_msgs[exc_code], taskid, bookId, imgId, tableId)
                                