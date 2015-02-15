REM registration
python setup.py register
REM Upload
python setup.py sdist upload
pause

REM if you want to upload without everytime registration, use .pypirc file in you home dir (~/.pypirc or C:\Users\YOU\.pypirc)