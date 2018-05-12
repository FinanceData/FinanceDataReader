
from setuptools import setup, find_packages

NAME = 'finance-datareader'
INSTALL_REQUIRES = (
    ['pandas>=0.19.2', 'requests>=2.3.0', 'requests-file', 'lxml']
)

setup(
    name = 'finance-datareader',
    version = '0.0.1',
    description = 'Financial data reader (price, stock list of markets)',
    author = 'FinanceData.KR',
    author_email = 'plusjune@financedata.kr',
    url = 'https://github.com/financedata/financedatareader',
    install_requires = INSTALL_REQUIRES,
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
    license='MIT License',
    python_requires  = '>=3',
    classifiers      = [
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        'Topic :: Scientific/Engineering',
    ],
    keywords = ['data', 'finance'],
    zip_safe=False,
)