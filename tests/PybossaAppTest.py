# -*- coding: utf-8 -*-
import app_tt.pb_apps.apps as apps
import os
import sys

script_path = os.path.abspath(os.path.dirname(__file__))

# strip off the file name to get the absolute path to proj
proj_path = os.path.dirname(script_path)
sys.path.append(os.path.join(proj_path, 'app_tt/pb_apps/tt_apps/'))

from ttapps import Apptt_select


def url_template_edit(server,file):
    text = ""
    for line in open(file).readlines():
        line = line.replace("#server",server)
        text += line
    return text

a = apps.Apptt("AppTeste", "testeapp", "Descricao app teste", "04d2d0f1-adf1-4ac0-8b3a-4bcb6bdcab19", "http://localhost:5000/")

a.set_template(url_template_edit("http://localhost/tt/", os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/app_tt/pb_apps/tt_apps/templates/template-meta.html"))

a.set_long_description(url_template_edit("http://localhost/tt/", os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/app_tt/pb_apps/tt_apps/templates/long_description-meta.html"))

infos = {"title" : "Titulo teste",
        "volume" : "1999"
        }

a.add_app_infos(infos)

ttselect = Apptt_select("ttselect-test")
