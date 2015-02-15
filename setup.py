"""
Package setup configuration needed for correct package creation
Taken from: https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications
"""

from distutils.core import setup

setup(
    # Application name:
    name="object-mapper",

    # Version number (initial):
    version="1.0.1",

    # Application author details:
    author="marazt",
    author_email="marazt@gmail.com",

    # Packages
    packages=[
        "mapper",
        "tests",
    ],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/marazt/object-mapper",

    #
    license="LICENSE.txt",
    description="ObjectMapper is a class for automatic object mapping. It helps you to create objects between\
                project layers (data layer, service layer, view) in a simple, transparent way.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "datetime",
        "nose",
    ],
)