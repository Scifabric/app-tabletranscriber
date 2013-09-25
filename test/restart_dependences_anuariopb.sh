#!/bin/bash

cd ..

#reload templates
. env/bin/activate
python app_tt/pb_apps/tt_apps/ttapps.py -u anuario1916pb_tt1
python app_tt/pb_apps/tt_apps/ttapps.py -u anuario1916pb_tt2
python app_tt/pb_apps/tt_apps/ttapps.py -u anuario1916pb_tt3
python app_tt/pb_apps/tt_apps/ttapps.py -u anuario1916pb_tt4
deactivate


sudo service rabbitmq-server stop
sudo service rabbitmq-server start
sudo service supervisor stop
sudo service supervisor start
sudo service apache2 restart
