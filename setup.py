import os
import sys
from setuptools import setup

python_2 = sys.version_info[0] == 2
def read(fname):
    with open(fname, 'rU' if python_2 else 'r') as fhandle:
        return fhandle.read()

version = '0.1.0'
required = [req.strip() for req in read('requirements.txt').splitlines() if req.strip()]
setup(
    name='rasp',
    version=version,
    author='Matthew Seal',
    author_email='mseal007@gmail.com',
    description='A collection of scripts and programs for managing a custom 3d printer enclosure',
    install_requires=required,
    license='MIT',
    packages=['rasp'],
    test_suite='tests',
    zip_safe=False,
    url='https://github.com/MSeal/raspberry_printer',
    download_url='https://github.com/MSeal/raspberry_printer/tarball/v' + version,
    keywords=['sensors', 'raspberry_pi', 'adafruit', 'scripting'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ]
)
