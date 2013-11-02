"""
django-admin-tools fork
"""

from setuptools import setup, find_packages

install_requires = [
    'django-admin-tools>=0.4.1',
    'BeautifulSoup>=3.2.0',
    'django-appconf>=0.4.1',
    'versiontools>=1.8.2',
    'django-mediagenerator==1.11',
]

setup(
    name='django-admintools-bootstrap',
    version=':versiontools:admintools_bootstrap:',
    url='https://github.com/spenoir/django-admintools-bootstrap',
    description='Bootstrap theme mediagenerator bundle for django admin',
    long_description=__doc__,
    setup_requires = [
        'versiontools >= 1.8.2',
    ],
    install_requires=install_requires,
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Operating System :: POSIX',
    ],
)
