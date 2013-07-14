#!/bin/sh

python setup.py install
pip install -r dev-requirements.txt
coverage run --source=werobot setup.py -q nosetests
if [ $? != 0 ]; then
    exit 1
fi
coverage html
coveralls