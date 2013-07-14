#!/bin/sh

python setup.py install
pip install -r dev-requirements.txt
coverage run --source=werobot setup.py -q nosetests
coverage html
coveralls