

code_report_tt1 = {
                "1" : "Problema de Submissão", 
                "2" : "Problema no carregamento da task atual", 
                "3" : "Problema no carregamento da próxima task",
                "4" : "Outro problema",
                "5" : "Descrição do outro problema"
                }

code_report_tt2 = {
                "1" : "Problema de Submissão", 
                "2" : "Problema no carregamento da task atual", 
                "3" : "Problema no carregamento da próxima task",
                "4" : "Outro problema",
                "5" : "Descrição do outro problema"
                }

code_report_tt3 = {
                "1" : "Problema de Submissão", 
                "2" : "Problema no carregamento da task atual", 
                "3" : "Problema no carregamento da próxima task",
                "4" : "Outro problema",
                "5" : "Descrição do outro problema"
                }

code_report_tt4 = {
                "1" : "Problema de Submissão", 
                "2" : "Problema no carregamento da task atual", 
                "3" : "Problema no carregamento da próxima task",
                "4" : "Outro problema",
                "5" : "Descrição do outro problema"
                }


def get_message_from_report(report_code, task_type):
    if task_type == "tt1":
        if code_report_tt1.has_key(report_code):
            return code_report_tt1[report_code]
        else:
            return ""
    elif task_type == "tt2":
        if  code_report_tt2.has_key(report_code):
            return code_report_tt2[report_code]
        else:
            return ""
    elif task_type == "tt3":
        if code_report_tt3.has_key(report_code):
            return code_report_tt3[report_code]
        else:
            return ""
    elif task_type == "tt4":
        if code_report_tt4.has_key(report_code):
            code_report_tt4[report_code]
        else:
            return ""
            
