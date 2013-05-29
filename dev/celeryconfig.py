from sqlalchemy import create_engine
engine = create_engine('postgresql://pybossa:lsdpybossa@localhost/celery')

## Broker settings.
BROKER_URL = "amqp://celery:celery@localhost:5672/celery"

# List of modules to import when celery starts.
CELERY_IMPORTS = ("app_tt.engine.tasks")

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = "amqp"
#CELERY_RESULT_DBURI = "postgresql://pybossa:lsdpybossa@localhost/celery"

