#!/bin/bash

#reload templates
. ../../env/bin/activate
python ../python/update_pyb_apps.py -u MemmoriaParaiba1841A1847_tt1
python ../python/update_pyb_apps.py -u MemmoriaParaiba1841A1847_tt2
python ../python/update_pyb_apps.py -u MemmoriaParaiba1841A1847_tt3
python ../python/update_pyb_apps.py -u MemmoriaParaiba1841A1847_tt4
deactivate

#sudo service rabbitmq-server stop
sudo service rabbitmq-server restart
sudo service supervisor stop
sudo service supervisor start
sudo service apache2 restart
