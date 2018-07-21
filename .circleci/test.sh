pip install virtualenv
virtualenv venv
./venv/bin/activate
pip install -r tox-requirements.txt
coverage run --source werobot -m py.test
pip install codecov
codecov
