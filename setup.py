# -*- coding: utf-8 -*-
from setuptools import setup
from os.path import join, isfile
from os import listdir

packages = [join('src', d) for d in listdir('src') if isfile(d)]

setup(
    name='child_ai',
    version='0.0.1',
    author=u'Ilya Kashkarev, Olga Nikitina',
    description=('working on a kaggle task'),
    keywords="AI, kaggle",
    url='https://github.com/kashkarik22i/child_ai',
    packages=packages,
    install_requires=['beautifulsoup4>=4.2.0',
                      'click>=3.2',
                      'nose2==0.5.0',
                      'regex==2014.02.16',
                      'wikitools==1.3',
    ],
    scripts=[]
)
