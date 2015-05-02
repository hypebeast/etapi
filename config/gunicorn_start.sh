#!/bin/bash

NAME="etapi"
FLASKDIR=/home/www/etapi
VENVDIR=/home/www/etapi/env
SOCKFILE=/homee/www/etapi/sock
USER=pi
GROUP=pi
NUM_WORKERS=1

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your unicorn
exec gunicorn etapi.app:create_app\(\) -b 127.0.0.1:8000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
