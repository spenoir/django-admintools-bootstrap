Django Admin Bootstrap theme
============================

Twitter Bootstrap support for Django Admin. Requires django-admin-tools package.


TODO:

* Fix some bugs
* Add multi-dropdown support

Screenshots
-----------

Some model admin

.. image:: https://bitbucket.org/salvator/django-admintools-bootstrap/raw/2a35c70ecb24/screenshot.png


Usage
-----

Install package::

 $ pip install -e hg+https://bitbucket.org/salvator/django-admintools-bootstrap#egg=admintools_bootstrap

Insert `admintools_bootstrap` to your INSTALLED_APPS before `admin_tools` and `django.contrib.admin` apps.
Make sure that `django.template.loaders.app_directories.Loader` are in the beginning of the `TEMPLATE_LOADERS` list.

Enjoy.


Site name in navigation bar and title
-------------------------------------

admintools-bootstrap can use current site to display site name in admin interface.

To enable this feature, add `django.contrib.sites` to your `INSTALLED_APPS` list (if you have not yet),
and `admintools_bootstrap.context_processors.site` to `TEMPLATE_CONTEXT_PROCESSORS` list.

Set site name and domain in `django.contrib.sites` admin.


Icons in menu items
-------------------

You can display icon from JQuery UI icon set on menu items. Add icon argument to MenuItem definition::

 items.AppList(
        _('Users'),
        models=('django.contrib.auth.*',),
        icon='ui-icon-person'
 )


Settings
--------

Site link::

 ADMINTOOLS_BOOTSTRAP_SITE_LINK = '/'

If not False, display link to site in the top panel


Used software:
--------------

* http://addyosmani.github.com/jquery-ui-bootstrap/
