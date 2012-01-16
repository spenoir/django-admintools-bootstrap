"""
django-admin-tools fork
"""

from setuptools import setup, find_packages

install_requires = [
    'django-admin-tools>=0.4.1',
    'BeautifulSoup>=3.2.0',
    'django-appconf>=0.4.1',
]

setup(
    name='django-admintools-bootstrap',
    version=':versiontools:appconf:',
    author='Dmitry Belyaev',
    author_email='ssalvator@gmail.com',
    url='https://bitbucket.org/salvator/django-admintools-bootstrap',
    description='Bootstrap theme for django admin',
    long_description=__doc__,
    install_requires=install_requires,
    packages=find_packages(),
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Operating System :: POSIX',
    ],
)
