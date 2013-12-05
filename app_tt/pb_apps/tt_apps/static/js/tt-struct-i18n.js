var en_US_dict = { 
    'question': "Please. Fix the lines and columns from the table.",
    'question_with_focus': "Please. Fix the lines and columns from the focused area in table.",
    'button_finished': "Save fixes",
    'button_rmline':  "Delete line",
    'button_rmseg': "Delete sement",
    'button_addline': "Add line",
    'button_addcolumn': "Add column",
    'button_mvseg': "Move segment",
    'button_mvline': "Move line",
    'task_name': "Task: ",
    'well_done': "Well done! ",
    'saved': "Your answer has been saved",
    'congratulations': "Congratulations! ",
    'finished': "All the tasks of struct fix have been completed!",
    'back': "Go back ",
    'other_apps': "or, Check other applications",
    'error': "Error! ",
    'err_msg': "Something went wrong, please contact the site administrators.",
    'workflowtask' : "There are other types of tasks available. Click to try it.",
    'progress-from' : "You have completed: ",
    'progress-to' : "tasks from"
}

var pt_dict= {
    'question': "Por favor. Corrija as linhas e colunas da tabela.",
    'question_with_focus': "Por favor. Corrija as linhas e colunas da área em foco da tabela.",
    'button_finished': "Salvar correções",
    'button_rmline':  "Remover linha",
    'button_rmseg': "Remover segmento",
    'button_addline': "Adicionar linha",
    'button_addcolumn': "Adicionar coluna",
    'button_mvseg': "Mover segmento",
    'button_mvline': "Mover linha",
    'task_name': "Tarefa: ",
    'well_done': "Muito bem! ",
    'saved': "Sua resposta foi salva",
    'congratulations': "Parabéns! ",
    'finished': "Todas as tarefas de correção de estrutura foram finalizadas",
    'back': "Voltar ",
    'other_apps': "ou, verificar outras aplicações",
    'error': "Erro! ",
    'err_msg': "Algo ocorreu errado, por favor contate o administrador do site.",
    'workflowtask' : "Há outros tipos de tarefas disponíveis. Clique para ir.",
    'progress-from' : "Você fez ",
    'progress-to' : "tarefas de "
    
}

var language = navigator.language? navigator.language : navigator.userLanguage;

switch(language){
	case 'en-US': var dict = en_US_dict;	break;
	case 'pt-BR': var dict = pt_dict; break;
	default: var dict = en_US_dict; 
}


$.i18n.setDictionary(dict);
