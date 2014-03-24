# -*- coding: utf-8 -*-
from app_tt.core import app as flask_app, pbclient
import ast
import requests
import json

def __fix_task_run_info_dict(d_str):
    d_str = d_str.replace('true', 'True')
    d_str = d_str.replace('false', 'False')
    
    return d_str

def __undo_fix_task_run_info_dict(info):
    if info.has_key('dataInicial'): # fix old error
        info.pop('dataInicial')
    if info.has_key('dataFinal'):  # fix old error
        info.pop('dataFinal')
    
    info['text']['girar'] = 'true' if info['text']['girar'] else 'false'
    
    if info['text'].has_key('nao_girar'):
        info['text']['nao_girar'] = 'true' if info['text']['nao_girar'] else 'false'
    else:
        info['text']['nao_girar'] = 'true'
    
    info['editable'] = 'true' if info['editable'] else 'false'
    
    return info

def __change_fields(info_dict):
    if not info_dict['text'].has_key('dataInicial'):
        info_dict['text']['dataInicial'] = ''
    if not info_dict['text'].has_key('dataFinal'):
        info_dict['text']['dataFinal'] = ''
    if info_dict.has_key('test'):
        info_dict.pop('test')
    
    return info_dict

def __update_taskrun(tr):
    print "tr.id: " + str(tr.id)
    print "tr.info: " + tr.info
    #print "api_key=" + str(flask_app.config['API_KEY'])
    #print "pybossa-url: " + flask_app.config['PYBOSSA_URL']
            
    r = requests.put("%s/api/taskrun/%s?api_key=%s" % 
                         (flask_app.config['PYBOSSA_URL'], tr.id, 
                          flask_app.config['API_KEY']),
                          data=json.dumps( dict(info=tr.info) ) )
        
    print "r: " + str(r.json())

def fix_dates_t2(app_short_name):
    apps = pbclient.find_app(short_name=app_short_name)
    
    if len(apps) > 0:
        app = pbclient.find_app(short_name=app_short_name)[0]
        trs = pbclient.find_taskruns(app.id)
        
        for tr in trs:
            infos = tr.info[1:len(tr.info)-1]
            infos = __fix_task_run_info_dict(infos)
            infos = ast.literal_eval(infos)
            
            if infos != "":
                if type(infos) is tuple:
                    info_list = []
                    for info in infos:
                        info = __change_fields(info)
                        info = __undo_fix_task_run_info_dict(info)
                        info_list.append(info)
                        
                    tr.info = json.dumps(tuple(info_list))        
                    
                elif type(infos) is dict:
                    info_dict = __change_fields(infos)
                
                    info_dict = __undo_fix_task_run_info_dict(info_dict)
                            
                    tr.info = "[" + json.dumps(info_dict) + "]"        
                    
                __update_taskrun(tr)
            
if __name__ == '__main__':
    short_names = ["caracterizaoeten2001bras_tt2",
                   "recenseamento1872pb_tt2",
                   "estatisticasdodi1949dist_tt2",
                   "rpparaiba1841_tt2",
                   "MemmoriaParaiba1841A1847_tt2",
                   "estatisticasdodi1950depa_tt2",
                   "anuario1916pb_tt2",
                   "mensagemdogovern1912gove_tt2",
                   "sinopse1937pb_tt2"]

    for sname in short_names:
        ntrs = fix_dates_t2(sname)
        