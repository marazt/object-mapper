#!/usr/bin/env bash
# Install Universal Wheels
pip install wheel
python setup.py bdist_wheel --universal
# Upload package by Twine
pip install twine
twine upload dist/*

# if you want to upload without everytime registration, use .pypirc file in you home dir (~/.pypirc or C:\Users\YOU\.pypirc)