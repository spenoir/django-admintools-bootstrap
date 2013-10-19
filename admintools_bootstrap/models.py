# monkey-pathching django admin

from django.conf import settings as django_settings
from django.contrib.admin import widgets
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from feincms.module.page import modeladmins
from django.utils.translation import ugettext_lazy as _


class FilteredSelectMultiple(forms.SelectMultiple):
    """
        removing 2 select fields widget
    """

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=[]):
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

widgets.FilteredSelectMultiple = FilteredSelectMultiple

class AdminDateWidget(forms.DateInput):

    def render(self, name, value, attrs=None):

        return

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vDateField', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminDateWidget, self).__init__(attrs=final_attrs, format=format)

widgets.AdminDateWidget = AdminDateWidget


class AdminTimeWidget(forms.TimeInput):

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vTimeField', 'size': '8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTimeWidget, self).__init__(attrs=final_attrs, format=format)

widgets.AdminTimeWidget = AdminTimeWidget


# patching admintools menu item
from admin_tools.menu import items

# addming icon argument to base MenuItem class
items.MenuItem.icon = None

import admintools_bootstrap.settings
