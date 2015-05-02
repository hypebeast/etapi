#!/bin/bash

FLASKDIR=/home/www/etapi
VENVDIR=/home/www/etapi/env

# activate the virtualenv
cd $VENVDIR
source bin/activate

cd $FLASKDIR

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Start the crawler
ETAPI_ENV=prod python scripts/crawler/crawler.py
