from setuptools import setup, find_packages

import cp_helper

setup(
    name='cp-helper',
    version=cp_helper.__version__,
    packages=find_packages(),
    long_description="Competitive programming helper",
    entry_points={
        'console_scripts': ['cp-helper = cp_helper.core:parse']
    },
    install_requires=[
        'beautifulsoup4>=4.7.1',
        'requests>=2.22.0',
        'docopt'
    ]
)
