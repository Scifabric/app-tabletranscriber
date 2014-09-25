var default_dict = { 
    'question': "Is there a table in this page?",
    'question-warning': "<i>*Don't worry if you think you’ve made a mistake, just keep contributing! Each task is executed by many volunteers – you are not alone!</i>",
    'book-info': "You're helping the transcription of the book:",
    'task-type': 'Selection task',
    'button_yes': " Yes",
    'button_no':  " No",
    'button_ntk': " I don't know",
    'task_name': "Task: ",
    'well_done': "Well done! ",
    'saved': "Your answer has been saved",
    'congratulations': "Congratulations! ",
    'finished': "All the selection tasks have been completed!",
    'back': "Go back ",
    'other_apps': "or, Check other applications",
    'error': "Error! ",
    'err_msg': "Something went wrong, please contact the site administrators.",
    'workflowtask' : "There is a new kind of task available. Click to try it.",
    'progress-from' : "You have already completed ",
    'progress-to' : "tasks – keep contributing!",
    'completed' : 'completed!',
    'completed-by-community' : 'completed by the community!',
    'completed-by-user' : 'completed by you!',
    'report-error-tooltip' : 'Have you found a error?',
    'page-tooltip' : 'Consider as a table any structure that has data for statistical purposes.',
    'remaining-tasks' : 'Remaining tasks'
};

var en_US_dict = default_dict;

var pt_dict= {
	    'question': "Existe uma tabela nessa página?",
	    'question-warning': "<i>*Não se preocupe se você acha que fez algo errado, continue contribuindo! Cada tarefa é executada por diversos voluntários – você não está sozinho!</i>",
	    'book-info': 'Você está ajudando a transcrever o livro:',
	    'task-type': 'Tarefa de seleção',
	    'button_yes': " Sim",
	    'button_no':  " Não",
	    'button_ntk': " Não sei",
	    'task_name': "Tarefa: ",
	    'well_done': "Muito bem! ",
	    'saved': "Sua resposta foi salva",
	    'congratulations': "Parabéns! ",
	    'finished': "Todas as tarefas de seleção foram finalizadas",
	    'back': "Voltar ",
	    'other_apps': "ou, verificar outras aplicações",
	    'error': "Erro! ",
	    'err_msg': "Algo ocorreu errado, por favor contate o administrador do site.",
        'workflowtask' : "Existe um novo tipo de tarefa disponível. Clique para ir.",
        'progress-from' : "Você já completou ",
        'progress-to' : "tarefas – continue contribuindo!",
        'completed' : 'finalizados!',
        'completed-by-community' : 'feitas pela comunidade!',
        'completed-by-user' : 'feitas por você!',
        'report-error-tooltip' : "Encontrou um erro?",
        'page-tooltip' : "Considere uma tabela qualquer estrutura que possua dados para fins estatísticos.",
        'remaining-tasks' : 'Tarefas restantes'
};

var language = navigator.language? navigator.language : navigator.userLanguage;

switch(language){
	case 'en-US': var t1_dict = en_US_dict;	break;
	case 'pt-BR': var t1_dict = pt_dict; break;
	default: var t1_dict = default_dict;
}

$.i18n.setDictionary(t1_dict);
