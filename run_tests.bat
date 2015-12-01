REM prerequisites: pip, virtualenv in path
virtualenv venv
cd venv/Scripts/
activate.bat & cd ../.. & pip install -r requirements.txt & nosetests tests --with-xunit --xunit-file=TEST-results.xml