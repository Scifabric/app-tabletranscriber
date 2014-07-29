var en_US_dict = { 
    'question': "Check the transcription of the highlighted cell and fix it if necessary. If the transcription is right, click on OK.",
    'question-warning': "<i>*Don't worry if you think you’ve made a mistake, just keep contributing! Each task is executed by many volunteers – you are not alone!</i>",
    'book-info': "You're helping the transcription of the book:",
    'task-type': 'Transcription task',
    'task_name': "Task: ",
    'well_done': "Well done! ",
    'saved': "Your answer has been saved",
    'congratulations': "Congratulations! ",
    'finished': "All the transcription tasks have been completed!",
    'back': "Go back ",
    'other_apps': "or, Check other applications",
    'error': "Error! ",
    'err_msg': "Something went wrong, please contact the site administrators.",
    'workflowtask' : "There are other types of tasks available. Click to try it.",
    'progress-from' : "You have already completed ",
    'progress-to' : "tasks – keep contributing!",
    'task-instruction-p1' : "<strong> Information </strong>",
    'task-instruction-p2' : "The <strong style='color: #339ACD'>blue</strong> cell is the one currently selected for checking its transcription;",
    'task-instruction-p3' : "The <strong style='color: #1BA038'>green</strong> cells show the transcriptions corrected by you or another user;",
    'task-instruction-p4' : "The <strong style='color: #E93F2D'>red</strong> cells show the transcriptions that need to be inspected and finished.",
    'task-instruction-p5' : "You can save the task any time. If you don't want to do the whole table transcription, you only need to click on <strong>Save fixes</strong>, so another user will continue from where you've stopped.",
    'button-finished-task' : 'Save fixes',
    'pc-transcription-p1' : 'Transcription made by a computer (',
    'pc-transcription-p2' : '% of confidence).',
    'human-transcription-label' : 'Transcription from another user',
    'your-transcription-label' : 'Your correction (if necessary)',
    'button-zoom-in' : 'Zoom In tool',
    'button-zoom-out' : 'Zoom Out tool',
    'button-help' : 'Open the help window',
    'button-previous-cell' : 'Previous cell',
    'button-next-cell' : 'Next cell',
    'completed' : 'completed!',
    'button_bug_report' : 'Point an error in the task',
    'completed-by-community' : 'completed by the community!',
    'completed-by-user' : 'completed by you!'

};

var pt_dict= {
    'question': "Verifique a transcrição do conteúdo da célula em destaque e corrija quando necessário. Se estiver adequada, clique em OK.",
    'question-warning': "<i>*Não se preocupe se você acha que fez algo errado, continue contribuindo! Cada tarefa é executada por diversos voluntários – você não está sozinho!</i>",
    'book-info': 'Você está ajudando a transcrever o livro:',
    'task-type': 'Tarefa de transcrição',
    'task_name': "Tarefa: ",
    'well_done': "Muito bem! ",
    'saved': "Sua resposta foi salva",
    'congratulations': "Parabéns! ",
    'finished': "Todas as tarefas de transcrição foram finalizadas",
    'back': "Voltar ",
    'other_apps': "ou, verificar outras aplicações",
    'error': "Erro! ",
    'err_msg': "Algo ocorreu errado, por favor contate o administrador do site.",
    'workflowtask' : "Há outros tipos de tarefas disponíveis. Clique para ir.",
    'progress-from' : "Você já completou ",
    'progress-to' : "tarefas – continue contribuindo!",
    'task-instruction-p1' : "<strong> Informações </strong>",
    'task-instruction-p2' : "A célula em <strong style='color: #339ACD'>azul</strong> é a célula atualmente selecionada para você verficar a transcrição;",
    'task-instruction-p3' : "Células em <strong style='color: #1BA038'>verde</strong> indicam transcrições corrigidas por você ou por outro usuário;",
    'task-instruction-p4' : "Células em <strong style='color: #E93F2D'>vermelho</strong> indicam transcrições que faltam ser inspecionadas e finalizadas.",
    'task-instruction-p5' : "Você pode salvar a tarefa a qualquer momento. Caso não queira fazer a transcrição da tabela inteira, basta clicar em <strong>Salvar correções</strong>, para que outro usuário continue de onde você parou.",
    'button-finished-task' : 'Salvar correções',
    'pc-transcription-p1' : 'Transcrição feita pelo computador (',
    'pc-transcription-p2' : '% de confiança).',
    'human-transcription-label' : 'Transcrição de outro usuário',
    'your-transcription-label' : 'Sua correção (se necessário)',
    'button-zoom-in' : 'Ferramenta de Zoom In',
    'button-zoom-out' : 'Ferramenta de Zoom Out',
    'button-help' : 'Abre a tela de ajuda',
    'button-previous-cell' : 'Célula anterior',
    'button-next-cell' : 'Próxima célula',
    'completed' : 'finalizados!',
    'button_bug_report' : 'Aponte um erro na tarefa',
    'completed-by-community' : 'feitas pela comunidade!',
    'completed-by-user' : 'feitas por você!'
};

var language = navigator.language? navigator.language : navigator.userLanguage;

switch(language){
	case 'en-US': var t4_dict = en_US_dict;	break;
	case 'pt-BR': var t4_dict = pt_dict; break;
	default: var t4_dict = en_US_dict; 
}

$.i18n.setDictionary(t4_dict);