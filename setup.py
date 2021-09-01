#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-playstore",
    version="0.0.1",
    description="Singer.io tap for extracting data from Google Play Store reports",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_playstore"],
    install_requires=[
        'singer-python>=5.12.1',
        'tap-gcs-csv @ git+https://github.com/fixdauto/tap-gcs-csv.git@9cb3c67561ba4a67512526e064248ba018695db3',
    ],
    entry_points="""
    [console_scripts]
    tap-playstore=tap_playstore:main
    """,
    packages=["tap_playstore"],
    package_data = {
        "catalog": ["tap_playstore/cached_catalog.json"]
    },
    include_package_data=True,
)
