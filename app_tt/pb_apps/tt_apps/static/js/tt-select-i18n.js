var default_dict = { 
    'question': "Is there a table in this page?",
    'button_yes': "Yes",
    'button_no':  "No",
    'button_ntk': "I don't know",
    'task_name': "Task: ",
    'saved': "Your answer has been saved",
    'congratulations': "Congratulations! ",
    'finished': "All the tasks have been completed!",
    'back': "Go back ",
    'other_apps': "or, Check other applications",
    'error': "Error! ",
    'err_msg': "Something went wrong, please contact the site administrators.",
    'workflowtask' : "There is a new kind of task available. Click to try it.",
    'progress-from' : "You have completed: ",
    'progress-to' : "tasks from"
}

var en_US_dict = default_dict;

var pt_dict= {
	    'question': "Existe uma tabela nessa página?",
	    'button_yes': "Sim",
	    'button_no':  "Não",
	    'button_ntk': "Não sei",
	    'task_name': "Tarefa: ",
	    'saved': "Sua resposta foi salva",
	    'congratulations': "Parabéns! ",
	    'finished': "Todas as tarefas foram finalizadas",
	    'back': "Voltar ",
	    'other_apps': "ou, verificar outras aplicações",
	    'error': "Erro! ",
	    'err_msg': "Algo ocorreu errado, por favor contate o administrador do site.",
            'workflowtask' : "Existe um novo tipo de tarefa disponível. Clique para ir.",
            'progress-from' : "Você fez ",
            'progress-to' : "tarefas de "
}

var language = navigator.language? navigator.language : navigator.userLanguage;

switch(language){
	case 'en-US': var dict = en_US_dict;	break;
	case 'pt-BR': var dict = pt_dict; break;
	default: var dict = default_dict;
}


$.i18n.setDictionary(dict);
