# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="Darknet Detector",
    version="0.0.2",
    author="Sara Falamaki",
    author_email = 'sara.falamaki@customerservice.nsw.gov.au',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description="Setup for running darknet_detector.py script",
    keywords = 'openalpr, nsw, anpr',
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/AlexeyAB/darknet",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        ],
    install_requires = [
        'numpy',
        'opencv-python',
        'Pillow'
        ],
    extras_require = {
        "dev": [
            "autopep8 ==1.4.4",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            ]
        },
    packages=find_packages(),
    )
