#!/bin/bash

sudo sh restart_dependences_allbooks.sh

sudo service rabbitmq-server stop
sudo service rabbitmq-server start

sudo service supervisor stop 
sudo service supervisor start
sudo service apache2 restart
