REM Install Universal Wheels
pip install wheel
python setup.py bdist_wheel --universal
REM Upload package by Twine
pip install twine
twine upload dist/*
pause

REM if you want to upload without everytime registration, use .pypirc file in you home dir (~/.pypirc or C:\Users\YOU\.pypirc)