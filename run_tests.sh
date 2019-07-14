#!bin/bash
# prerequisites: pip, virtualenv in path
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
nose2 tests --plugin nose2.plugins.junitxml --config myconfig.cfg