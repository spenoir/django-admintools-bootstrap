# monkey-pathching django admin

from django.contrib.admin import widgets
from django import forms
from django.template.loader import render_to_string
from django.utils.html import format_html


class FilteredSelectMultiple(forms.SelectMultiple):
    """
        removing 2 select fields widget
    """

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=[]):
        super(FilteredSelectMultiple, self).__init__(attrs, choices)


class AdminDateWidget(forms.DateInput):

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'attrs': attrs
        }
        return render_to_string(
            'admin/widgets/_admin_date_widget.html',
            dictionary=context
        )


class AdminTimeWidget(forms.TimeInput):

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'attrs': attrs
        }
        return render_to_string(
            'admin/widgets/_admin_date_widget_mirror.html',
            dictionary=context
        )


class AdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return format_html('%s%s' % (rendered_widgets[0],rendered_widgets[1]))

widgets.FilteredSelectMultiple = FilteredSelectMultiple
widgets.AdminDateWidget = AdminDateWidget
widgets.AdminTimeWidget = AdminTimeWidget
widgets.AdminSplitDateTime = AdminSplitDateTime


# patching admintools menu item
from admin_tools.menu import items

# addming icon argument to base MenuItem class
items.MenuItem.icon = None

import admintools_bootstrap.settings
