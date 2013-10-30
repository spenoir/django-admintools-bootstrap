Django Admin Bootstrap theme
============================

Twitter Bootstrap support for Django Admin. Requires django-admin-tools and mediagenerator packages.
It also requires SASS to be installed.

This module started out life here:

https://bitbucket.org/salvator/django-admintools-bootstrap

I've developed it to fit into my preferred Django stack that includes mediagenerator and SASS.
I've also updated to Bootstrap 3 and fixed a few bugs, as well as restyling things and including Glyphicons.


Screenshots
-----------

.. image:: screen-shot-2013-10-29.png
.. image:: screen-shot-2013-10-20.2.png

Usage
-----

Install package::

 $ pip install -e hg+https://github.com/spenoir/django-admintools-bootstrap#egg=admintools_bootstrap

* Insert `admintools_bootstrap` to your INSTALLED_APPS before `admin_tools` and `django.contrib.admin` apps.
* Make sure you have static files application installed and configured. See https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/ for details.
* Enjoy.


Site name in navigation bar and title
-------------------------------------

admintools-bootstrap can use current site to display site name in admin interface.

To enable this feature, add `django.contrib.sites` to your `INSTALLED_APPS` list (if you have not yet).

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

If not False, display specified link to site in the top panel

Media generator bundles are created for admin.js and admin.css.

Used software:
--------------

* http://addyosmani.github.com/jquery-ui-bootstrap/
* http://twitter.github.com/bootstrap/
* https://bitbucket.org/izi/django-admin-tools/
* http://www.crummy.com/software/BeautifulSoup/
* https://github.com/jezdez/django-appconf
* http://pypi.python.org/pypi/versiontools
* https://bitbucket.org/wkornewald/django-mediagenerator/
* http://sass-lang.com/

TODO
----

* Fix some bugs
* Add multi-dropdown support
