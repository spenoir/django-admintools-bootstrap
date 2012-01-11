"""
django-admin-tools fork
"""

from setuptools import setup, find_packages

install_requires = [
    'django-admin-tools>=0.4.1',
]

setup(
    name='django-admintools-bootstrap',
    version='0.1-pre-Alpha',
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
