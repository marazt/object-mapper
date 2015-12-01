#!bin/bash
# prerequisites: pip, virtualenv in path
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
nosetests tests --with-xunit --xunit-file=TEST-results.xml