# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='child_ai',
    version='0.0.1',
    author=u'Ilya Kashkarev, Olga Nikitina',
    description=('Working on a kaggle task'),
    keywords="AI, kaggle",
    url='https://github.com/kashkarik22i/child_ai',
    packages=find_packages(),
    install_requires=['beautifulsoup4>=4.2.0',
                      'click>=3.2',
                      'nose2==0.5.0',
                      'regex==2014.02.16',
                      'wikitools==1.3',
                      'pycrypto==2.6.1',
    ],
    entry_points='''
        [console_scripts]
        cipher=scripts.cipher_data:cli
    ''',
    scripts=[]
)
