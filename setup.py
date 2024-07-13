from setuptools import setup, find_packages

setup(
    name='FinanceDataReader',
    version='0.1.0',
    author='loopinf',
    author_email='loopinf@gmail.com',
    description='A package for fetching and visualizing financial data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/loopinf/FinanceDataReader',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'bs4',
        'tqdm',
        'plotly',
        # Add any other dependencies your package needs
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)