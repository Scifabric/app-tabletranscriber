

code_report_tt1 = {
                "1" : unicode("Problema de Submissão","utf-8"), 
                "2" : unicode("Problema no carregamento da task atual", "utf-8"), 
                "3" : unicode("Problema no carregamento da próxima task","utf-8"),
                "4" : unicode("Outro problema","utf-8"),
                "5" : unicode("Descrição do outro problema","utf-8")
                }

code_report_tt2 = {
                "1" : unicode("Problema de Submissão","utf-8"), 
                "2" : unicode("Problema no carregamento da task atual","utf-8"), 
                "3" : unicode("Problema no carregamento da próxima task","utf-8"),
                "4" : unicode("Não há tabela na página", "utf-8"),
                "5" : unicode("Não consigo ver o conteúdo da página do livro", "utf-8"),
                "6" : unicode("Outro problema","utf-8"),
                "7" : unicode("Descrição do outro problema","utf-8")
                }

code_report_tt3 = {
                "1" : unicode("Problema de Submissão","utf-8"), 
                "2" : unicode("Problema no carregamento da task atual","utf-8"), 
                "3" : unicode("Problema no carregamento da próxima task","utf-8"),
                "4" : unicode("Não entendi como usar as ferramentas","utf-8"),
                "5" : unicode("Não consigo deletar uma linha ou coluna para formar uma célula válida","utf-8"),
                "6" : unicode("Outro problema","utf-8"),
                "7" : unicode("Descrição do outro problema","utf-8")
                }

code_report_tt4 = {
                "1" : unicode("Problema de Submissão","utf-8"), 
                "2" : unicode("Problema no carregamento da task atual","utf-8"), 
                "3" : unicode("Problema no carregamento da próxima task","utf-8"),
                "4" : unicode("Não consigo ler o conteúdo da célula","utf-8"),
                "5" : unicode("A célula está cortada","utf-8"),
                "6" : unicode("Outro problema","utf-8"),
                "7" : unicode("Descrição do outro problema","utf-8")
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
            
