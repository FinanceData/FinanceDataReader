from setuptools import setup, find_packages
import os.path
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name             = 'finance-datareader',
    version          = '0.9.34',
    description      = 'The FinanceDataReader is financial data reader(crawler) for finance.',
    long_description = long_description,
    author           = 'plusjune',
    author_email     = 'plusjune@financedata.kr',
    url              = 'https://github.com/financedata-org/FinanceDataReader',
    download_url     = 'https://github.com/financedata-org/FinanceDataReader/archive/master.zip',
    install_requires = ['bokeh', 'plotly', 'backtrader', 'matplotlib==3.2.2'],
    packages         = find_packages(exclude=['docs', 'tutorial']),
    keywords         = ['trading', 'development', 'stock', 'data-analysis'],
    python_requires  = '>=3',
    package_data     =  {},
    zip_safe=False,
    license='GPLv3+',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        # Indicate which Topics are covered by the package
        'Topic :: Software Development',
        'Topic :: Office/Business :: Financial',

        # Pick your license as you wish (should match "license" above)
        ('License :: OSI Approved :: ' +
         'GNU General Public License v3 or later (GPLv3+)'),

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 지원하는 버전 명시, 버전이 다르다고 실행이 안되는건 아님
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        # Operating Systems on which it runs
        'Operating System :: OS Independent',
    ],
)