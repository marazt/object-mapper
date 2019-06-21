REM prerequisites: pip, virtualenv in path
virtualenv venv
cd venv/Scripts/
activate.bat & cd ../.. & pip install -r requirements.txt & nose2 tests --plugin nose2.plugins.junitxml --config myconfig.cfg