# -*- coding: utf-8 -*-

from setuptools import setup

project = "etapi"

setup(
    name=project,
    version='0.1.0',
    url='https://github.com/hypebeast/etapi',
    description='Eta PI is a Raspberry PI based, Flask powered monitor for ETA Heizkessels.',
    author='Sebastian Ruml',
    author_email='sebastian.ruml@gmail.com',
    packages=["etapi"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
