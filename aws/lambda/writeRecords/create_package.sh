#!/bin/bash

FUNC_NAME=writeRecords
DIR=$(pwd)
PACKAGE_DIR=venv/lib/python3.5/site-packages

if [ -f "$FUNC_NAME.zip" ]; then
    echo "$FUNC_NAME.zip already exists. Nothing to do. Exiting"
    exit 1
fi

#if [ -d "venv" ]; then
#    echo "venv already exists"
#else
#    echo "creating virtualenv venv" 
#    virtualenv -p python3 venv
#fi

#source venv/bin/activate
#pip install requests
#deactivate

#if [ ! -d "$PACKAGE_DIR" ]; then
#    echo "error: $PACKAGE_DIR does not exist"
#    exit 1
#fi

echo "creating zip package"
zip -r9 $DIR/$FUNC_NAME.zip psycopg2
zip -ur $FUNC_NAME.zip $FUNC_NAME.py

