# Check the official documentation http://flask.pocoo.org/docs/deploying/mod_wsgi/
# Activate the virtual env (we assume that virtualenv is in the env folder)
activate_this = '/local/adabriand/pybossa_apps/app-tabletranscriber/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import logging, sys
sys.stdout = sys.stderr
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/local/adabriand/pybossa_apps/app-tabletranscriber')
# Run the web-app
from app_tt.application import app as application
