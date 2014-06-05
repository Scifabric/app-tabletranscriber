from app_tt.core import pbclient
from tests.app_tt.base import submit_answer, done_task
import sys
import time

def create_t2_task(test_case, book_id, task_t1):
    # creating an answer for the T1 app
    task_run = dict(app_id=task_t1.app_id, task_id=task_t1.id, info="Yes")

    # Anonymous submission
    submit_answer(test_case.base_url, task_run)
    
    # FB authenticated user submission
    task_run['facebook_user_id'] = '12345'
    submit_answer(test_case.base_url, task_run)
    
    # Signalling the T1 task completion
    done_task(test_case.app, task_t1.id)
    time.sleep(5)
    
    # check if T1 task is closed
    task_t1 = pbclient.get_tasks(task_t1.app_id, sys.maxint)[0]
    test_case.assertTrue(task_t1.state == "completed")
    
    # one task from T2 app should exist
    app_t2 = pbclient.find_app(short_name=book_id + "_tt2")
    test_case.assertTrue(len(app_t2) > 0, "Error tt_app was not created")
    
    t2_tasks = pbclient.get_tasks(app_t2[0].id, sys.maxint)
    test_case.assertTrue(len(t2_tasks) == 1)
    
    return t2_tasks[0]

def create_t3_task(test_case, book_id, task_t2):
    # creating an answer for the T2 app
    answer_t2 = '[{\"id\":\"new\",\"top\":244,\"left\":24,\"width\":506,\"height\":177,\"text\":{\"titulo\":\"test-titulo\",\"subtitulo\":\"test-subtitulo\",\"assunto\":\"0\",\"fontes\":\"test-fontes\",\"outros\":\"\",\"dataInicial\":\"01/01/1901\",\"dataFinal\":\"01/01/1902\",\"girar\":false,\"nao_girar\":true},\"editable\":true}, {\"id\":\"new\",\"top\":100,\"left\":300,\"width\":250,\"height\":230,\"text\":{\"titulo\":\"test-titulo\",\"subtitulo\":\"test-subtitulo\",\"assunto\":\"3\",\"fontes\":\"test-fontes\",\"outros\":\"test-outros\",\"dataInicial\":\"01/01/1901\",\"dataFinal\":\"01/01/1902\",\"girar\":false,\"nao_girar\":true},\"editable\":true}]'
    task_run = dict(app_id=task_t2.app_id, task_id=task_t2.id, info=answer_t2)
    
    # Anonymous submission
    submit_answer(test_case.base_url, task_run)
    
    # FB authenticated user submission
    task_run['facebook_user_id'] = '12345'
    submit_answer(test_case.base_url, task_run)
    
    # Signalling the T2 task completion
    done_task(test_case.app, task_t2.id)
    time.sleep(15)
    
    # check if T2 task is closed
    task_t2 = pbclient.get_tasks(task_t2.app_id, sys.maxint)[0]
    test_case.assertTrue(task_t2.state == "completed")
    
    # one task from T3 app should exist
    app_t3 = pbclient.find_app(short_name=book_id + "_tt3")
    test_case.assertTrue(len(app_t3) > 0, "Error tt_app was not created")
    
    t3_tasks = pbclient.get_tasks(app_t3[0].id, sys.maxint)
    test_case.assertTrue(len(t3_tasks) == 2)
    
    return t3_tasks


def create_t4_task(test_case, book_id, task_t3, number_of_expected_t4_tasks):
    # creating an answer for the T3 app
    answer_t3 = '{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}'
    task_run = dict(app_id=task_t3.app_id, task_id=task_t3.id, info=answer_t3)
    
    # Anonymous submission
    submit_answer(test_case.base_url, task_run)
    
    # FB authenticated user submission
    task_run['facebook_user_id'] = '12345'
    submit_answer(test_case.base_url, task_run)
    
    # Signalling the T3 task completion
    done_task(test_case.app, task_t3.id)
    time.sleep(10)
    
    # check if T3 task is closed
    task_t3 = pbclient.get_tasks(task_t3.app_id, sys.maxint)[0]
    test_case.assertTrue(task_t3.state == "completed")
    
    # one task from T4 app should exist
    app_t4 = pbclient.find_app(short_name=book_id + "_tt4")
    test_case.assertTrue(len(app_t4) > 0, "Error tt_app was not created")
    
    t4_tasks = pbclient.get_tasks(app_t4[0].id, sys.maxint)
    test_case.assertTrue(len(t4_tasks) == number_of_expected_t4_tasks)
    
    return t4_tasks


def close_t4_task(test_case, book_id, task_t4):
    # creating an answer for the T4 app
    answer_t4 = '{\"cells\":[[0,0,239,54],[239,0,507,54],[0,54,239,103],[239,54,507,103],[0,103,239,178],[239,103,507,178]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\",\"MENSAGEM ..\u00c7 19\",\"DE SETEMBRO DE 1918.\"],\"human_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\",\"MENSAGEM ..\u00c7 19\",\"DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81,72,85],\"num_of_confirmations\":[2,2,2,2,2,2]}'
    task_run = dict(app_id=task_t4.app_id, task_id=task_t4.id, info=answer_t4)
    
    # Anonymous submission
    submit_answer(test_case.base_url, task_run)
    
    # FB authenticated user submission
    task_run['facebook_user_id'] = '12345'
    submit_answer(test_case.base_url, task_run)
    
    # Signalling the T3 task completion
    done_task(test_case.app, task_t4.id)
    time.sleep(1)
    
    # check if T4 task is closed
    tasks_t4 = pbclient.get_tasks(task_t4.app_id, sys.maxint)
    
    for task in tasks_t4:
        test_case.assertTrue(task.state == "completed")
    
