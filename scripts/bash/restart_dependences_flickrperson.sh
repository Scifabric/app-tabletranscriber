#!/bin/bash

#reload templates
. ../../env/bin/activate
python ../app-flickrperson/createTasks.py -s http://localhost/pybossa -k 9134c60c-1caa-4935-8eb0-15f3527809de -c
python ../app-flickrperson/createTasks.py -t ../app-flickrperson/static/fb-templates/template.html
deactivate

sudo service apache2 restart
